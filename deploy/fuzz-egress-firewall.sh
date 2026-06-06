#!/usr/bin/env bash
# Firewall the mwgg-fuzz-egress bridge.
#
# Fuzz containers run UNTRUSTED world code with internet egress, so they must not
# reach the host, the private network, or the cloud metadata endpoint — they only
# need GitHub / PyPI / FUZZ_WHEEL_HOSTS. We filter in the DOCKER-USER iptables
# chain: Docker jumps to it before its own FORWARD rules and never flushes it, so
# our rules survive `docker` restarts (a host reboot clears them — re-run then,
# e.g. via the bundled systemd unit).
#
# Idempotent: builds a private chain from scratch each run and hooks it once.
#
#   sudo /usr/local/sbin/fuzz-egress-firewall.sh
#   sudo MWGG_FUZZ_BLOCK_IPS="203.0.113.5" /usr/local/sbin/fuzz-egress-firewall.sh   # also block host IP(s)
set -euo pipefail

# The fuzz network's bridge interface. Pin it when creating the network so this
# stays stable:  docker network create --opt com.docker.network.bridge.name=mwgg-fuzz0 mwgg-fuzz-egress
BRIDGE="${MWGG_FUZZ_BRIDGE:-mwgg-fuzz0}"
CHAIN="MWGG-FUZZ-EGRESS"
# Optional space-separated host public IP(s) to also block (the RFC1918 drops
# already cover the host's private/bridge-gateway address).
HOST_PUBLIC_IPS="${MWGG_FUZZ_BLOCK_IPS:-}"

# Wait for the bridge (Docker recreates it on daemon start; tolerate a boot race).
for _ in $(seq 1 30); do
  ip link show "$BRIDGE" >/dev/null 2>&1 && break
  sleep 1
done
if ! ip link show "$BRIDGE" >/dev/null 2>&1; then
  echo "error: bridge '$BRIDGE' not found. Create the network first:" >&2
  echo "  docker network create --opt com.docker.network.bridge.name=$BRIDGE mwgg-fuzz-egress" >&2
  exit 1
fi

# (Re)build our chain so re-running never stacks duplicates.
iptables -N "$CHAIN" 2>/dev/null || true
iptables -F "$CHAIN"

# Let already-vetted flows back (replies to allowed egress).
iptables -A "$CHAIN" -m conntrack --ctstate ESTABLISHED,RELATED -j RETURN

# Hard-block: cloud metadata + link-local, every RFC1918 range, and CGNAT.
for net in 169.254.0.0/16 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 100.64.0.0/10; do
  iptables -A "$CHAIN" -d "$net" -j DROP
done
# Optionally block the host's own public IP(s).
for ip in $HOST_PUBLIC_IPS; do
  iptables -A "$CHAIN" -d "$ip" -j DROP
done

# Everything else (the public internet) is allowed.
iptables -A "$CHAIN" -j RETURN

# Hook the chain into DOCKER-USER for traffic coming FROM the fuzz bridge.
iptables -C DOCKER-USER -i "$BRIDGE" -j "$CHAIN" 2>/dev/null \
  || iptables -I DOCKER-USER -i "$BRIDGE" -j "$CHAIN"

echo "applied: $BRIDGE -> $CHAIN (metadata + RFC1918 + CGNAT${HOST_PUBLIC_IPS:+ + host IPs} dropped; rest allowed)"
