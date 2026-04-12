(function () {
    "use strict";

    const chatMessages = document.getElementById("chat-messages");
    const chatInput = document.getElementById("chat-input");
    const chatSendBtn = document.getElementById("chat-send-btn");
    const generateBtn = document.getElementById("generate-btn");
    const leaveBtn = document.getElementById("leave-btn");
    const abandonBtn = document.getElementById("abandon-btn");
    const lockBtn = document.getElementById("lock-btn");
    const settingsEditBtn = document.getElementById("settings-edit-btn");
    const yamlFileInput = document.getElementById("yaml-file-input");
    const dropZone = document.getElementById("yaml-upload-drop");
    const generateStandard = document.getElementById("generate-standard");
    const generateCustom = document.getElementById("generate-custom");
    const downloadPackageBtn = document.getElementById("download-package-btn");
    const uploadGameZone = document.getElementById("upload-game-zone");
    const gameFileInput = document.getElementById("game-file-input");
    const apworldQueuePanel = document.getElementById("apworld-queue-panel");
    const apworldQueueList = document.getElementById("apworld-queue-list");
    const apworldQueueEmpty = document.getElementById("apworld-queue-empty");
    const isViewer = typeof IS_VIEWER !== "undefined" && IS_VIEWER;

    let pollTimer = null;
    let pollInterval = isViewer ? 15000 : 3000;
    let idleCycles = 0;
    let currentPlayerCount = 0;
    let maxYamlsHeld = 0;
    let knownVersion = null;
    let pollErrorCount = 0;
    let lastReadyCount = 0;
    let lastTotalCount = 0;
    let lastPendingRequestCount = null;
    let lastApworldVersions = {};  // game_name -> world_version
    let allowCustomApworlds = false;
    const renderedMessageIds = new Set();

    // Returns { fast, slow, idleThreshold } based on lobby size / viewer mode.
    // Viewer:       15s → 60s after 4 idle cycles
    // Small lobby  (<20 players): 3s → 10s after ~15s idle
    // Large lobby (>=20 players): 10s → 30s after ~60s idle
    function getPollTiers() {
        if (isViewer) {
            return { fast: 15000, slow: 60000, idleThreshold: 4 };
        }
        if (currentPlayerCount >= 20) {
            return { fast: 10000, slow: 30000, idleThreshold: 6 };
        }
        return { fast: 3000, slow: 10000, idleThreshold: 5 };
    }

    function scrollChatToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    scrollChatToBottom();

    function pollStatus() {
        fetch(API_BASE + "/status?after_message=" + lastMessageId)
            .then(res => res.json())
            .then(data => {
                knownVersion = data.version;
                currentState = data.state;
                hasCustomYamls = data.has_custom || false;
                allowCustomApworlds = !!data.allow_custom_apworlds;
                updatePlayers(data.players);
                appendMessages(data.messages);
                updateGenerateButton(data);
                updateStatusDisplay(data);
                if (MY_PLAYER_ID !== null && data.apworlds) {
                    const currentVersions = {};
                    const apworldOwnerYamls = new Set();
                    (data.apworlds || []).forEach(a => {
                        currentVersions[a.game_name] = a.world_version || "custom";
                        apworldOwnerYamls.add(a.yaml_id);
                    });

                    const myPlayer = data.players.find(p => p.id === MY_PLAYER_ID);
                    if (myPlayer && Object.keys(lastApworldVersions).length > 0) {
                        const myYamls = myPlayer.yamls || [];
                        const myYamlIds = new Set(myYamls.map(y => y.id));
                        const myGames = new Set(myYamls.map(y => y.game).filter(Boolean));
                        const alerts = [];
                        myGames.forEach(game => {
                            const oldVer = lastApworldVersions[game];
                            const newVer = currentVersions[game];
                            if (oldVer === newVer) return;
                            const ownsNew = (data.apworlds || []).some(
                                a => a.game_name === game && myYamlIds.has(a.yaml_id)
                            );
                            if (ownsNew) return;
                            if (newVer && !oldVer) {
                                alerts.push(`${game}: custom APWorld v${newVer} is now active`);
                            } else if (!newVer && oldVer) {
                                alerts.push(`${game}: custom APWorld was removed, reverted to server version`);
                            } else if (newVer && oldVer) {
                                alerts.push(`${game}: APWorld changed from v${oldVer} to v${newVer}`);
                            }
                        });
                        if (alerts.length > 0) {
                            alert("APWorld change affecting your game(s):\n" + alerts.join("\n"));
                        }
                    }
                    lastApworldVersions = currentVersions;
                }

                if (IS_OWNER && !isViewer &&
                    (data.state === LOBBY_STATE_OPEN || data.state === LOBBY_STATE_LOCKED)) {
                    const pendingCount = Number.isInteger(data.pending_request_count)
                        ? data.pending_request_count : 0;
                    if (pendingCount <= 0) {
                        if (lastPendingRequestCount !== 0) {
                            renderApworldRequests([]);
                        }
                    } else if (lastPendingRequestCount !== pendingCount) {
                        loadApworldRequests();
                    }
                    lastPendingRequestCount = pendingCount;
                } else {
                    lastPendingRequestCount = null;
                }

                if (MY_PLAYER_ID !== null &&
                    (currentState === LOBBY_STATE_OPEN || currentState === LOBBY_STATE_LOCKED || currentState === LOBBY_STATE_GENERATING)) {
                    const stillMember = data.players.some(p => p.id === MY_PLAYER_ID);
                    if (!stillMember) {
                        clearInterval(pollTimer);
                        document.getElementById("lobby-container").innerHTML =
                            '<h2>You have been removed from this lobby.</h2>' +
                            '<a href="/lobbies" class="lobby-back-link">&larr; Back to lobby list</a>';
                        return;
                    }
                }

                if (data.state === LOBBY_STATE_DONE) {
                    showResult(data);
                } else if (data.state === LOBBY_STATE_CLOSED) {
                    document.getElementById("lobby-container").innerHTML =
                        '<h1>Lobby Expired</h1><p>This lobby has been closed due to inactivity.</p>' +
                        '<p><a href="/lobbies">Back to Lobbies</a></p>';
                    clearInterval(pollTimer);
                    return;
                }

                currentPlayerCount = data.players.length;
                lastReadyCount = data.ready_count || 0;
                lastTotalCount = data.player_count || 0;
                pollErrorCount = 0;

                if (isViewer) {
                    const viewerJoin = document.getElementById("lobby-viewer-join");
                    if (viewerJoin) {
                        const canJoin = data.state === LOBBY_STATE_OPEN &&
                            (data.max_players === 0 || data.player_count < data.max_players);
                        viewerJoin.style.display = canJoin ? "" : "none";
                    }
                }
            })
            .catch(err => {
                pollErrorCount++;
                console.error("Poll error:", err);
                if (pollErrorCount >= 3) {
                    clearInterval(pollTimer);
                    alert("Connection to the lobby was lost after repeated failures. Please refresh the page to reconnect.");
                }
            });
    }

    function pingAndMaybePoll() {
        fetch(API_BASE + "/ping")
            .then(res => res.json())
            .then(data => {
                const stateChanged = data.state !== currentState;
                const versionChanged = data.version !== knownVersion;
                knownVersion = data.version;
                if (currentState === LOBBY_STATE_GENERATING || currentState === LOBBY_STATE_LOCKED || stateChanged || versionChanged) {
                    idleCycles = 0;
                    pollStatus();
                } else {
                    idleCycles++;
                    adjustPollInterval();
                }
            })
            .catch(err => console.error("Ping error:", err));
    }

    function adjustPollInterval() {
        const tiers = getPollTiers();
        const newInterval = idleCycles >= tiers.idleThreshold ? tiers.slow : tiers.fast;
        if (newInterval !== pollInterval) {
            pollInterval = newInterval;
            clearInterval(pollTimer);
            pollTimer = setInterval(pingAndMaybePoll, pollInterval);
        }
    }

    function resetPollRate() {
        idleCycles = 0;
        const fast = getPollTiers().fast;
        if (pollInterval !== fast) {
            pollInterval = fast;
            clearInterval(pollTimer);
            pollTimer = setInterval(pingAndMaybePoll, pollInterval);
        }
    }

    function updatePlayers(players) {
        const playerList = document.getElementById("lobby-players");
        if (!playerList) return;

        maxYamlsHeld = Math.max(0, ...players.map(p => p.yamls ? p.yamls.length : 0));
        playerList.innerHTML = "";
        players.forEach(p => {
            const li = document.createElement("li");
            li.className = "lobby-player";
            li.dataset.playerId = p.id;

            let html = '<div class="lobby-player-header">';
            const yamlCount = p.yamls ? p.yamls.length : 0;
            const readyTick = p.is_ready ? ' <span class="ready-indicator" title="Ready">✓</span>' : '';
            const yamlCountLabel = ` <span class="player-yaml-count">${yamlCount}/${MAX_YAMLS_PER_PLAYER}${readyTick}</span>`;
            html += `<strong>${escapeHtml(p.name)}${p.is_owner ? " (Host)" : ""}${yamlCountLabel}</strong>`;
            if (IS_OWNER && !p.is_owner && (currentState === LOBBY_STATE_OPEN || currentState === LOBBY_STATE_LOCKED)) {
                html += `<button class="kick-btn" data-player-id="${p.id}" title="Kick player">Kick</button>`;
            }
            if (!isViewer && p.id === MY_PLAYER_ID && (currentState === LOBBY_STATE_OPEN || currentState === LOBBY_STATE_LOCKED)) {
                const readyClass = p.is_ready ? " ready-btn-on" : "";
                const readyLabel = p.is_ready ? "Ready ✓" : "Mark Ready";
                const hasYamls = p.yamls && p.yamls.length > 0;
                const disabledAttr = hasYamls ? "" : " disabled title=\"Upload at least one YAML first\"";
                html += `<button class="ready-btn${readyClass}"${disabledAttr} data-player-id="${p.id}">${readyLabel}</button>`;
            }
            html += '</div>';
            html += '<ul class="player-yamls">';
            p.yamls.forEach(y => {
                const slotName = escapeHtml(y.player_name || '');
                const isCustom = !!y.is_custom;
                const apwMissing = isCustom && !y.apworld;
                const customTag = isCustom
                    ? `<span class="yaml-custom-tag${apwMissing ? ' yaml-custom-tag-missing' : ''}" title="${apwMissing ? 'APWorld missing' : 'Custom APWorld'}">&#x1F9E9;</span>`
                    : '';
                // Server world version tag for standard worlds — hidden once an upgrade apworld is uploaded
                const hasUpgradeApworld = !isCustom && !!y.apworld;
                const versionSatisfied = !isCustom && y.required_version && !y.version_warning
                    && !y.version_upgrade_available && !hasUpgradeApworld;
                const serverVer = !isCustom && y.server_world_version && !hasUpgradeApworld && !versionSatisfied
                    ? `<span class="yaml-world-version" title="Server has v${escapeHtml(y.server_world_version)} — compatibility unverified (YAML has no version requirement)">v${escapeHtml(y.server_world_version)}</span>`
                    : '';
                const versionWarn = y.version_warning && !hasUpgradeApworld
                    ? `<span class="yaml-version-warning" title="${escapeHtml(y.version_warning)}">&#9888;</span>`
                    : '';
                // Puzzle-piece tag for upgrade apworlds, with dual-version tooltip
                const upgradeTag = hasUpgradeApworld ? (() => {
                    const uploadedVer = y.apworld.world_version ? `v${y.apworld.world_version}` : null;
                    const srvVer = y.server_world_version ? `v${y.server_world_version}` : null;
                    const tip = (uploadedVer && srvVer)
                        ? `Upgraded APWorld: ${uploadedVer} (server: ${srvVer})`
                        : 'Upgraded APWorld';
                    return `<span class="yaml-custom-tag" title="${escapeHtml(tip)}">&#x1F9E9;</span>`;
                })() : '';
                const gameDisplay = y.game
                    ? (isCustom || hasUpgradeApworld
                        ? `<span class="yaml-game-name yaml-game-custom">${escapeHtml(y.game)}</span>`
                        : `<a class="yaml-game-name" href="/games/${encodeURIComponent(y.game)}/player-options">${escapeHtml(y.game)}</a>`)
                    : `<span class="yaml-game-name">${escapeHtml(y.filename)}</span>`;
                const downloadHref = `/api/lobby/${LOBBY_ID}/yaml/${y.id}`;
                html += `<li data-yaml-id="${y.id}">`;
                html += `<span class="yaml-slot-name" data-tooltip="${escapeHtml(y.filename)}"><span>${slotName}</span></span>`;
                html += customTag;
                html += upgradeTag;
                html += gameDisplay;
                html += serverVer;
                html += versionWarn;

                const hasOwnApworld = !!y.apworld_is_own;
                const hasPendingRequest = !!y.apworld_request_pending;
                const canEditApworld = p.id === MY_PLAYER_ID && allowCustomApworlds && !hasOwnApworld && !hasPendingRequest;

                if (isCustom && (currentState === LOBBY_STATE_OPEN || currentState === LOBBY_STATE_LOCKED)) {
                    const apw = y.apworld;
                    if (apw) {
                        const verLabel = apw.world_version ? `v${escapeHtml(apw.world_version)}` : "APWorld";
                        let apwTip = escapeHtml(apw.filename);
                        if (apw.world_version && y.required_version) {
                            apwTip += ` — v${escapeHtml(apw.world_version)} satisfies requirement v${escapeHtml(y.required_version)}`;
                        } else if (apw.world_version) {
                            apwTip += ` — v${escapeHtml(apw.world_version)}, compatibility unverified (YAML has no version requirement)`;
                        }
                        html += `<span class="apworld-status-ok" title="${apwTip}">&#10003; ${verLabel}</span>`;
                    } else if (!canEditApworld && !hasPendingRequest) {
                        html += `<span class="apworld-missing" title="APWorld not yet uploaded">&#9888;</span>`;
                    }
                    if (hasPendingRequest && p.id === MY_PLAYER_ID) {
                        html += `<button class="apworld-upload-btn" disabled title="APWorld replacement request is pending host approval">In Review</button>`;
                    } else if (canEditApworld) {
                        const reqVer = y.required_version ? ` (requires v${escapeHtml(y.required_version)})` : "";
                        html += `<button class="apworld-upload-btn" data-yaml-id="${y.id}" title="Upload APWorld for this game${reqVer}">&#x2B06; Replace APWorld</button>`;
                    }
                }

                if (!isCustom && (currentState === LOBBY_STATE_OPEN || currentState === LOBBY_STATE_LOCKED)) {
                    if (hasUpgradeApworld) {
                        const apw = y.apworld;
                        const verLabel = apw.world_version ? `v${escapeHtml(apw.world_version)}` : "APWorld";
                        let apwTip = escapeHtml(apw.filename);
                        if (apw.world_version && y.required_version) {
                            apwTip += ` — v${escapeHtml(apw.world_version)} satisfies requirement v${escapeHtml(y.required_version)}`;
                            if (y.server_world_version) {
                                apwTip += ` (server has v${escapeHtml(y.server_world_version)})`;
                            }
                        }
                        html += `<span class="apworld-status-ok" title="${apwTip}">&#10003; ${verLabel}</span>`;
                    } else if (versionSatisfied) {
                        html += `<span class="apworld-status-ok" title="Server v${escapeHtml(y.server_world_version)} satisfies requirement v${escapeHtml(y.required_version)}">&#10003; v${escapeHtml(y.server_world_version)}</span>`;
                    }
                    if (hasPendingRequest && p.id === MY_PLAYER_ID) {
                        html += `<button class="apworld-upload-btn" disabled title="APWorld replacement request is pending host approval">In Review</button>`;
                    } else if (canEditApworld) {
                        const reqVer = y.required_version ? ` (requires v${escapeHtml(y.required_version)})` : "";
                        html += `<button class="apworld-upload-btn" data-yaml-id="${y.id}" title="Upload APWorld replacement${reqVer}">&#x2B06; Replace APWorld</button>`;
                    }
                }

                html += `<span class="yaml-actions">`;
                html += `<a class="yaml-download-btn" href="${downloadHref}" title="Download YAML" download>&#x2B07;</a>`;
                html += `<button class="yaml-view-btn" data-yaml-id="${y.id}" data-filename="${escapeHtml(y.filename)}" title="View YAML">&#128065;</button>`;
                if ((currentState === LOBBY_STATE_OPEN || currentState === LOBBY_STATE_LOCKED) && (IS_OWNER || p.id === MY_PLAYER_ID)) {
                    html += `<button class="yaml-delete-btn" data-yaml-id="${y.id}" title="Remove YAML">&times;</button>`;
                }
                html += `</span>`;
                html += '</li>';
            });
            html += '</ul>';

            li.innerHTML = html;
            playerList.appendChild(li);
        });

        // Re-bind delete, kick, apworld upload, ready, and view buttons
        bindYamlDeleteButtons();
        bindKickButtons();
        bindApworldUploadButtons();
        bindReadyButtons();
        bindYamlViewButtons();
    }

    function buildMessageDiv(msg) {
        const div = document.createElement("div");
        div.className = "chat-msg" + (msg.system ? " chat-system" : "");
        div.dataset.messageId = msg.id;
        const time = new Date(msg.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const isTrueSystem = msg.system && msg.sender === "System";
        const deleteBtn = (!isTrueSystem && IS_OWNER)
            ? `<button class="msg-delete-btn" data-message-id="${msg.id}" title="Delete message">&times;</button>`
            : "";
        if (isTrueSystem) {
            div.innerHTML = `<span class="chat-time-col"><span class="chat-time">${time}</span></span><span class="chat-system-text">${escapeHtml(msg.content)}</span>`;
        } else {
            div.innerHTML = `<span class="chat-time-col"><span class="chat-time">${time}</span>${deleteBtn}</span><span class="chat-content"><strong class="chat-sender">${escapeHtml(msg.sender)}:</strong> <span class="chat-text">${escapeHtml(msg.content)}</span></span>`;
        }
        return div;
    }

    function insertMessageInOrder(div, msgId) {
        const existing = chatMessages.querySelectorAll(".chat-msg[data-message-id]");
        for (const el of existing) {
            if (parseInt(el.dataset.messageId, 10) > msgId) {
                chatMessages.insertBefore(div, el);
                return;
            }
        }
        chatMessages.appendChild(div);
    }

    function appendMessages(messages) {
        if (!chatMessages || !messages.length) return;
        messages.forEach(msg => {
            if (msg.id > lastMessageId) lastMessageId = msg.id;
            if (renderedMessageIds.has(msg.id)) return;
            if (isViewer && !msg.system) return;
            renderedMessageIds.add(msg.id);
            insertMessageInOrder(buildMessageDiv(msg), msg.id);
        });
        scrollChatToBottom();
    }

    function updateGenerateButton(data) {
        const info = document.getElementById("generate-info");
        if (info) {
            const maxP = data.max_players > 0 ? `/${data.max_players}` : "";
            info.textContent = `Players: ${data.player_count}${maxP} | YAMLs: ${data.total_yamls} | Ready: ${data.ready_count}/${data.player_count}`;
        }

        const isCustomMode = hasCustomYamls && (currentState === LOBBY_STATE_OPEN || currentState === LOBBY_STATE_LOCKED);
        if (generateStandard) generateStandard.style.display = isCustomMode ? "none" : "";
        if (generateCustom) generateCustom.style.display = isCustomMode ? "" : "none";

        const incompleteNotice = document.getElementById("package-incomplete-notice");
        const missingNotice = document.getElementById("missing-apworlds-notice");
        const missingList = document.getElementById("missing-apworlds-list");
        const upgradeNotice = document.getElementById("upgrade-apworlds-notice");
        const upgradeList = document.getElementById("upgrade-apworlds-list");
        if (isCustomMode) {
            const missingGames = new Set();
            const upgradeGames = new Map(); // game name → version_warning string
            (data.players || []).forEach(p => {
                (p.yamls || []).forEach(y => {
                    if (y.is_custom && !y.apworld) {
                        missingGames.add(y.game || y.filename);
                    }
                    if (y.version_upgrade_available && !y.apworld) {
                        upgradeGames.set(y.game || y.filename, y.version_warning || null);
                    }
                });
            });
            const isIncomplete = missingGames.size > 0 || upgradeGames.size > 0;
            if (incompleteNotice) incompleteNotice.style.display = isIncomplete ? "" : "none";
            if (missingNotice && missingList) {
                if (missingGames.size > 0) {
                    missingList.innerHTML = [...missingGames]
                        .map(g => `<li>${escapeHtml(g)}</li>`).join("");
                    missingNotice.style.display = "";
                } else {
                    missingNotice.style.display = "none";
                }
            }
            if (upgradeNotice && upgradeList) {
                if (upgradeGames.size > 0) {
                    upgradeList.innerHTML = [...upgradeGames]
                        .map(([g, warn]) => `<li>${escapeHtml(g)}${warn ? ` <span style="opacity:0.75">(${escapeHtml(warn)})</span>` : ''}</li>`)
                        .join("");
                    upgradeNotice.style.display = "";
                } else {
                    upgradeNotice.style.display = "none";
                }
            }
        } else {
            if (incompleteNotice) incompleteNotice.style.display = "none";
            if (missingNotice) missingNotice.style.display = "none";
            if (upgradeNotice) upgradeNotice.style.display = "none";
        }

        if (generateBtn) {
            const hasYamls = data.total_yamls > 0;
            generateBtn.disabled = !hasYamls || (currentState !== LOBBY_STATE_OPEN && currentState !== LOBBY_STATE_LOCKED);
            if (currentState === LOBBY_STATE_GENERATING) {
                generateBtn.textContent = "Generating...";
                generateBtn.disabled = true;
            } else {
                generateBtn.textContent = "Generate Seed";
            }
        }
    }

    function formatTimeout(minutes) {
        if (minutes < 60) return minutes + ' min';
        if (minutes < 1440) return Math.round(minutes / 60) + ' hr';
        const days = Math.round(minutes / 1440);
        return days + (days === 1 ? ' day' : ' days');
    }

    function formatMetaOpts(s, g) {
        const hm = s.hint_mode || 'default';
        const hmLabel = hm === 'default' ? 'full' : hm === 'own' ? 'hide own' : hm === 'all' ? 'hide all' : hm;
        const hc = s.hint_cost != null ? s.hint_cost : 5;
        const hcLabel = hc > 100 ? 'off' : hc + '%';
        const sp = g.spoiler != null ? g.spoiler : 0;
        const spLabel = sp === 0 ? 'off' : sp === 1 ? 'on' : sp === 2 ? '+playthrough' : 'full';
        return `Release: ${s.release_mode || '?'} | Collect: ${s.collect_mode || '?'} | Remaining: ${s.remaining_mode || '?'} | Hints: ${hmLabel} @ ${hcLabel} | Item Cheat: ${s.item_cheat ? 'on' : 'off'} | Spoiler: ${spLabel}`;
    }

    function updateStatusDisplay(data) {
        const statusEl = document.getElementById("lobby-status");
        if (!statusEl) return;

        statusEl.className = "lobby-status-" + data.state;
        if (data.state === LOBBY_STATE_OPEN) statusEl.textContent = "Open";
        else if (data.state === LOBBY_STATE_GENERATING) statusEl.textContent = "Generating...";
        else if (data.state === LOBBY_STATE_DONE) statusEl.textContent = "Seed created, Lobby locked";
        else if (data.state === LOBBY_STATE_CLOSED) statusEl.textContent = "Closed";
        else if (data.state === LOBBY_STATE_LOCKED) statusEl.textContent = "Locked";

        if (data.max_yamls_per_player != null) {
            MAX_YAMLS_PER_PLAYER = data.max_yamls_per_player;
        }
        if (data.timeout_minutes != null) {
            TIMEOUT_MINUTES = data.timeout_minutes;
        }

        const titleEl = document.getElementById("lobby-title");
        if (titleEl && data.title) titleEl.textContent = data.title;

        const metaMain = document.getElementById("lobby-meta-main");
        if (metaMain && data.max_yamls_per_player != null) {
            const race = data.race ? "Race Mode | " : "";
            const customAP = data.allow_custom_apworlds ? "Custom APWorlds: enabled" : "Custom APWorlds: disabled";
            metaMain.textContent = `Max YAMLs: ${data.max_yamls_per_player} | Timeout: ${formatTimeout(data.timeout_minutes)} | ${race}${customAP}`;
        }

        const playerBadge = document.getElementById("player-count-badge");
        if (playerBadge && data.player_count != null) {
            const maxP = data.max_players > 0 ? `/${data.max_players}` : "";
            playerBadge.textContent = `(${data.player_count}${maxP})`;
        }

        const metaOpts = document.getElementById("lobby-meta-opts");
        if (metaOpts && data.server_opts) {
            metaOpts.textContent = formatMetaOpts(data.server_opts, data.gen_opts || {});
        }

        const expiryEl = document.getElementById("lobby-expiry");
        if (expiryEl && data.last_activity) {
            const expiryMs = new Date(data.last_activity).getTime() + TIMEOUT_MINUTES * 60000;
            expiryEl.textContent = "Expires: " + new Date(expiryMs).toLocaleString();
        }

        const isActiveState = data.state === LOBBY_STATE_OPEN || data.state === LOBBY_STATE_LOCKED;

        const generateInfo = document.getElementById("generate-info");
        if (generateInfo) generateInfo.style.display = isActiveState ? "" : "none";

        const uploadArea = document.getElementById("yaml-upload-area");
        if (uploadArea) {
            uploadArea.style.display = isActiveState ? "" : "none";
        }

        const genSection = document.getElementById("lobby-generate");
        if (genSection) {
            genSection.style.display = isActiveState ? "" : "none";
        }
        if (apworldQueuePanel && !isActiveState) {
            apworldQueuePanel.style.display = "none";
        }

        const generatingDiv = document.getElementById("lobby-generating");
        if (generatingDiv) {
            generatingDiv.style.display = data.state === LOBBY_STATE_GENERATING ? "block" : "none";
        }

        const isGeneratingOrDone = data.state === LOBBY_STATE_GENERATING || data.state === LOBBY_STATE_DONE;
        if (leaveBtn) {
            leaveBtn.style.display = data.state === LOBBY_STATE_OPEN ? "" : "none";
        }
        if (abandonBtn) {
            abandonBtn.style.display = isGeneratingOrDone ? "none" : "";
        }
        if (lockBtn) {
            lockBtn.style.display = isActiveState ? "" : "none";
            if (data.state === LOBBY_STATE_LOCKED) {
                lockBtn.textContent = "Unlock Lobby";
            } else {
                lockBtn.textContent = "Lock Lobby";
            }
        }
        if (settingsEditBtn) {
            settingsEditBtn.style.display = isActiveState ? "" : "none";
        }
    }

    function showResult(data) {
        const resultDiv = document.getElementById("lobby-result");
        if (!resultDiv) return;

        let html = '<h2>Seed Ready!</h2>';
        if (IS_OWNER && data.seed_id) {
            html += `<p><a href="/seed/${escapeHtml(data.seed_id)}">View Seed</a></p>`;
        }
        if (data.room_id) {
            html += `<p><a href="/room/${escapeHtml(data.room_id)}" class="lobby-btn lobby-btn-primary">Go to Room</a></p>`;
        }
        if (IS_OWNER && data.server_password) {
            html += `<p class="server-password-row">Server Password:
                <span class="server-password-reveal">
                    <span class="password-placeholder">hover to reveal</span>
                    <span class="password-value">${escapeHtml(data.server_password)}</span>
                </span></p>`;
        }
        resultDiv.innerHTML = html;
        resultDiv.style.display = "block";
    }

    function sendChat() {
        if (!chatInput) return;
        const message = chatInput.value.trim();
        if (!message) return;

        resetPollRate();
        fetch(API_BASE + "/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        })
            .then(res => res.json())
            .then(data => {
                if (!data.error) {
                    chatInput.value = "";

                    if (!renderedMessageIds.has(data.id)) {
                        renderedMessageIds.add(data.id);
                        insertMessageInOrder(buildMessageDiv(data), data.id);
                        scrollChatToBottom();
                    }
                }
            })
            .catch(err => console.error("Chat error:", err));
    }

    if (chatSendBtn) {
        chatSendBtn.addEventListener("click", sendChat);
    }
    if (chatInput) {
        chatInput.addEventListener("keypress", e => {
            if (e.key === "Enter") sendChat();
        });
    }

    if (chatMessages && IS_OWNER) {
        chatMessages.addEventListener("click", e => {
            const btn = e.target.closest(".msg-delete-btn");
            if (!btn) return;
            const messageId = btn.dataset.messageId;
            if (!confirm("Delete this message?")) return;

            fetch(`${API_BASE}/message/${messageId}`, { method: "DELETE" })
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        const div = chatMessages.querySelector(`[data-message-id="${messageId}"]`);
                        if (div) {
                            div.className = "chat-msg chat-system";
                            const timeEl = div.querySelector(".chat-time");
                            const timeHtml = timeEl ? timeEl.outerHTML : "";
                            div.innerHTML = `<span class="chat-time-col">${timeHtml}</span><span class="chat-system-text">${escapeHtml(data.content)}</span>`;
                        }
                    }
                })
                .catch(err => console.error("Message delete error:", err));
        });
    }

    function uploadFiles(files) {
        if (!files || files.length === 0) return;

        const formData = new FormData();
        for (const file of files) {
            formData.append("file", file);
        }

        fetch(API_BASE + "/upload", {
            method: "POST",
            body: formData,
        })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert("Upload error: " + data.error);
                } else {
                    if (yamlFileInput) yamlFileInput.value = "";
                    const customUploaded = (data.uploaded || []).filter(u => u.is_custom);
                    if (customUploaded.length > 0) {
                        const lines = customUploaded.map(u => {
                            const ver = u.required_version ? ` v${u.required_version}` : "";
                            return `  • ${u.game}${ver}`;
                        });
                        alert(
                            `Uploaded ${customUploaded.length} custom game YAML(s):\n` +
                            lines.join("\n") + "\n\n" +
                            `Please upload the corresponding .apworld file(s) using the ` +
                            `"⬆ Replace APWorld" button next to each custom YAML. ` +
                            `You can also drag and drop an .apworld file directly onto the button.`
                        );
                    }
                    if (data.upgrades_needed && data.upgrades_needed.length > 0) {
                        const lines = data.upgrades_needed.map(u =>
                            `  • ${u.game} (requires v${u.required_version})`
                        );
                        alert(
                            "Your YAML requires a newer version of the following game(s):\n" +
                            lines.join("\n") + "\n\n" +
                            "Please upload an updated APWorld using the \"⬆ Replace APWorld\" button next to your YAML. " +
                            "You can also drag and drop an .apworld file directly onto the button."
                        );
                    }
                    if (data.active_apworld_notices && data.active_apworld_notices.length > 0) {
                        alert(
                            "Note: A custom APWorld is already active for the following game(s):\n" +
                            data.active_apworld_notices.join("\n") + "\n\n" +
                            "Your YAML will use the active custom APWorld version, not the server version."
                        );
                    }
                    if (data.version_warnings && data.version_warnings.length > 0) {
                        alert("Version mismatch detected:\n" + data.version_warnings.join("\n"));
                    }
                    resetPollRate();
                    pollStatus();
                }
            })
            .catch(err => {
                console.error("Upload error:", err);
                alert("Upload failed. Please try again.");
            });
    }

    if (yamlFileInput) {
        yamlFileInput.addEventListener("change", e => {
            if (e.target.files.length > 0) uploadFiles(e.target.files);
        });
    }

    const APWORLD_MAX_BYTES = 60 * 1024 * 1024; // must match server-side APWORLD_MAX_SIZE

    function formatImpactSummary(preview) {
        const game = preview && preview.game_name ? preview.game_name : "Unknown game";
        const candidateVersion = preview && preview.candidate_world_version
            ? `v${preview.candidate_world_version}` : "custom version";
        const impactedPlayers = (preview && preview.impacted_players) || [];
        const impactedCount = preview && preview.impacted_player_count
            ? preview.impacted_player_count : impactedPlayers.length;
        const deletions = (preview && preview.would_delete_yamls) || [];
        const lines = [
            `Replace APWorld for '${game}' with ${candidateVersion}?`,
            "",
        ];
        if (impactedCount > 0) {
            lines.push(`Affected players (${impactedCount}): ${impactedPlayers.join(", ") || "unknown"}`);
        } else {
            lines.push("No players are affected.");
        }
        if (deletions.length > 0) {
            lines.push("");
            lines.push("The following YAMLs will be removed as incompatible:");
            deletions.forEach(y => {
                const who = y.player_name || "Unknown";
                const file = y.filename || `YAML #${y.yaml_id}`;
                const req = y.required_version ? ` (requires v${y.required_version})` : "";
                lines.push(`- ${who}: ${file}${req}`);
            });
        }
        lines.push("");
        lines.push("Continue?");
        return lines.join("\n");
    }

    async function postApworld(yamlId, file, mode, extraFields) {
        const formData = new FormData();
        if (file) {
            formData.append("file", file);
        }
        formData.append("mode", mode);
        Object.entries(extraFields || {}).forEach(([key, value]) => {
            if (value !== undefined && value !== null && value !== "") {
                formData.append(key, String(value));
            }
        });
        const res = await fetch(`${API_BASE}/apworld/${yamlId}`, { method: "POST", body: formData });
        let data = {};
        try {
            data = await res.json();
        } catch (_e) {
            data = {};
        }
        return { status: res.status, data };
    }

    async function applyApworldWithHash(yamlId, previewToken, preview, impactHash, confirmImpact, depth) {
        const attempt = depth || 0;
        if (attempt > 4) {
            alert("APWorld apply failed because impact data kept changing. Please try again.");
            return;
        }

        const { status, data } = await postApworld(yamlId, null, "apply", {
            impact_hash: impactHash,
            confirm_impact: confirmImpact ? 1 : 0,
            preview_token: previewToken,
        });

        if (status === 409 || status === 412) {
            const newPreview = data.impact_preview || preview;
            const newHash = data.impact_hash;
            if (!newHash) {
                alert(data.error || "APWorld apply requires a refreshed confirmation.");
                return;
            }
            if (IS_OWNER && newPreview && newPreview.affects_other_players) {
                if (!confirm(formatImpactSummary(newPreview))) return;
                return applyApworldWithHash(yamlId, previewToken, newPreview, newHash, true, attempt + 1);
            }
            alert(data.error || "Impact preview changed. Please try again.");
            return;
        }

        if (data.error) {
            alert("APWorld upload error: " + data.error);
            return;
        }

        if (data.pending_approval) {
            alert("APWorld replacement request submitted for host approval.");
        }

        resetPollRate();
        pollStatus();
    }

    async function uploadApworld(yamlId, file) {
        if (file.size > APWORLD_MAX_BYTES) {
            alert(`APWorld file is too large (${(file.size / (1024 * 1024)).toFixed(1)} MB). The maximum allowed size is 60 MB.`);
            return;
        }

        try {
            const previewResult = await postApworld(yamlId, file, "preview");
            if (previewResult.status === 413) {
                alert("APWorld file is too large. The maximum allowed size is 60 MB.");
                return;
            }
            if (previewResult.data.error) {
                alert("APWorld upload error: " + previewResult.data.error);
                return;
            }

            const preview = previewResult.data.impact_preview || {};
            const impactHash = previewResult.data.impact_hash;
            const previewToken = previewResult.data.preview_token;
            if (!impactHash) {
                alert("APWorld preview failed: missing impact hash.");
                return;
            }
            if (!previewToken) {
                alert("APWorld preview failed: missing preview token.");
                return;
            }

            let confirmImpact = false;
            if (IS_OWNER && preview.affects_other_players) {
                if (!confirm(formatImpactSummary(preview))) return;
                confirmImpact = true;
            }

            await applyApworldWithHash(yamlId, previewToken, preview, impactHash, confirmImpact, 0);
        } catch (err) {
            console.error("APWorld upload error:", err);
            alert("APWorld upload failed. Please try again.");
        }
    }

    async function postApworldRequestAction(requestId, action, payload) {
        const res = await fetch(`${API_BASE}/apworld-request/${requestId}/${action}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload || {}),
        });
        let data = {};
        try {
            data = await res.json();
        } catch (_e) {
            data = {};
        }
        return { status: res.status, data };
    }

    async function approveApworldRequest(requestId, impactHash, preview, depth) {
        const attempt = depth || 0;
        if (attempt > 4) {
            alert("APWorld approval failed because impact data kept changing. Please try again.");
            return;
        }
        if (!confirm(formatImpactSummary(preview))) return;
        const { status, data } = await postApworldRequestAction(requestId, "approve", { impact_hash: impactHash });
        if (status === 409) {
            const updatedPreview = data.impact_preview || preview;
            const updatedHash = data.impact_hash;
            if (!updatedHash) {
                alert(data.error || "Request approval needs refreshed preview.");
                return;
            }
            if (!confirm(formatImpactSummary(updatedPreview))) return;
            return approveApworldRequest(requestId, updatedHash, updatedPreview, attempt + 1);
        }
        if (data.error) {
            alert(data.error);
            return;
        }
        resetPollRate();
        pollStatus();
    }

    async function rejectApworldRequest(requestId) {
        if (!confirm("Reject this APWorld request?")) return;
        const { data } = await postApworldRequestAction(requestId, "reject", {});
        if (data.error) {
            alert(data.error);
            return;
        }
        resetPollRate();
        pollStatus();
    }

    function bindApworldQueueButtons() {
        document.querySelectorAll(".apworld-request-approve-btn").forEach(btn => {
            btn.addEventListener("click", function () {
                const requestId = this.dataset.requestId;
                const impactHash = this.dataset.impactHash;
                const previewRaw = this.dataset.impactPreview || "{}";
                let preview = {};
                try {
                    preview = JSON.parse(previewRaw);
                } catch (_e) {
                    preview = {};
                }
                approveApworldRequest(requestId, impactHash, preview, 0);
            });
        });
        document.querySelectorAll(".apworld-request-reject-btn").forEach(btn => {
            btn.addEventListener("click", function () {
                rejectApworldRequest(this.dataset.requestId);
            });
        });
    }

    function renderApworldRequests(requests) {
        if (!apworldQueuePanel || !apworldQueueList || !apworldQueueEmpty) return;
        const rows = requests || [];
        if (!rows.length) {
            apworldQueuePanel.style.display = "none";
            apworldQueueList.innerHTML = "";
            apworldQueueEmpty.style.display = "none";
            return;
        }

        apworldQueuePanel.style.display = "";
        apworldQueueEmpty.style.display = "none";
        apworldQueueList.innerHTML = rows.map(r => {
            const preview = r.impact_preview || {};
            const version = r.world_version ? `v${escapeHtml(r.world_version)}` : "custom";
            const currentVer = preview.active_world_version
                ? `v${escapeHtml(preview.active_world_version)}` : null;
            const currentSource = preview.active_source === "server" ? "server" : "custom";
            const fromLabel = currentVer ? ` from ${currentSource} ${currentVer}` : "";
            const impacted = preview.impacted_player_count || 0;
            const deletions = (preview.would_delete_yaml_ids || []).length;
            return `<li class="apworld-request-item">
                <div class="apworld-request-main">
                    <strong>${escapeHtml(r.requester_name)}</strong> wants to replace
                    <strong>${escapeHtml(r.game_name)}</strong>${fromLabel} with ${escapeHtml(version)}.
                    <div class="apworld-request-meta">Affected players: ${impacted} | YAML deletions: ${deletions}</div>
                </div>
                <div class="apworld-request-actions">
                    <button class="lobby-btn lobby-btn-primary apworld-request-approve-btn"
                        data-request-id="${r.id}"
                        data-impact-hash="${escapeHtml(r.impact_hash || "")}"
                        data-impact-preview='${JSON.stringify(preview).replace(/&/g, "&amp;").replace(/'/g, "&#39;")}'>
                        Approve
                    </button>
                    <button class="lobby-btn lobby-btn-danger apworld-request-reject-btn" data-request-id="${r.id}">
                        Reject
                    </button>
                </div>
            </li>`;
        }).join("");
        bindApworldQueueButtons();
    }

    function loadApworldRequests() {
        if (!IS_OWNER || !apworldQueuePanel) return;
        fetch(`${API_BASE}/apworld-requests`)
            .then(res => res.json())
            .then(data => {
                if (data.error) return;
                renderApworldRequests(data.requests || []);
            })
            .catch(err => console.error("APWorld request poll error:", err));
    }

    function bindApworldUploadButtons() {
        document.querySelectorAll(".apworld-upload-btn").forEach(btn => {
            const yamlId = btn.dataset.yamlId;

            btn.addEventListener("click", function () {
                const input = document.createElement("input");
                input.type = "file";
                input.accept = ".apworld";
                input.onchange = e => {
                    const file = e.target.files[0];
                    if (file) uploadApworld(yamlId, file);
                };
                input.click();
            });

            btn.addEventListener("dragenter", e => {
                e.preventDefault();
                e.stopPropagation();
                btn.classList.add("apworld-upload-btn--drag");
            });

            btn.addEventListener("dragover", e => {
                e.preventDefault();
                e.stopPropagation();
                e.dataTransfer.dropEffect = "copy";
            });

            btn.addEventListener("dragleave", () => {
                btn.classList.remove("apworld-upload-btn--drag");
            });

            btn.addEventListener("drop", e => {
                e.preventDefault();
                e.stopPropagation();
                btn.classList.remove("apworld-upload-btn--drag");
                const file = e.dataTransfer.files[0];
                if (file) uploadApworld(yamlId, file);
            });
        });
    }
    bindApworldUploadButtons();

    if (downloadPackageBtn) {
        downloadPackageBtn.addEventListener("click", () => {
            if (lastReadyCount < lastTotalCount) {
                const unready = lastTotalCount - lastReadyCount;
                if (!confirm(`${unready} player(s) are not ready yet. Download package anyway?`)) return;
            }
            window.location.href = `${API_BASE}/download-package`;
        });
    }

    function uploadGameFile(file) {
        const formData = new FormData();
        formData.append("file", file);

        if (uploadGameZone) uploadGameZone.classList.add("uploading");

        fetch(`${API_BASE}/upload-game`, { method: "POST", body: formData })
            .then(res => res.json())
            .then(data => {
                if (uploadGameZone) uploadGameZone.classList.remove("uploading");
                if (data.error) {
                    alert("Upload error: " + data.error);
                } else {
                    resetPollRate();
                    pollStatus();
                }
            })
            .catch(err => {
                if (uploadGameZone) uploadGameZone.classList.remove("uploading");
                console.error("Game upload error:", err);
                alert("Upload failed. Please try again.");
            });
    }

    if (uploadGameZone) {
        uploadGameZone.addEventListener("dragover", e => {
            e.preventDefault();
            uploadGameZone.classList.add("drag-over");
        });
        uploadGameZone.addEventListener("dragleave", () => {
            uploadGameZone.classList.remove("drag-over");
        });
        uploadGameZone.addEventListener("drop", e => {
            e.preventDefault();
            uploadGameZone.classList.remove("drag-over");
            if (e.dataTransfer.files.length > 0) uploadGameFile(e.dataTransfer.files[0]);
        });
    }

    if (gameFileInput) {
        gameFileInput.addEventListener("change", e => {
            if (e.target.files.length > 0) uploadGameFile(e.target.files[0]);
        });
    }

    if (dropZone) {
        dropZone.addEventListener("dragover", e => {
            e.preventDefault();
            dropZone.classList.add("drag-over");
        });
        dropZone.addEventListener("dragleave", () => {
            dropZone.classList.remove("drag-over");
        });
        dropZone.addEventListener("drop", e => {
            e.preventDefault();
            dropZone.classList.remove("drag-over");
            uploadFiles(e.dataTransfer.files);
        });
    }

    function bindYamlDeleteButtons() {
        document.querySelectorAll(".yaml-delete-btn").forEach(btn => {
            btn.addEventListener("click", function () {
                const yamlId = this.dataset.yamlId;
                if (!confirm("Remove this YAML?")) return;

                resetPollRate();
                fetch(API_BASE + "/yaml/" + yamlId, { method: "DELETE" })
                    .then(res => res.json())
                    .then(data => {
                        if (data.error) alert(data.error);
                        else pollStatus();
                    })
                    .catch(err => console.error("Delete error:", err));
            });
        });
    }
    bindYamlDeleteButtons();

    function bindKickButtons() {
        document.querySelectorAll(".kick-btn").forEach(btn => {
            btn.addEventListener("click", function () {
                const playerId = this.dataset.playerId;
                if (!confirm("Kick this player?")) return;

                resetPollRate();
                fetch(API_BASE + "/kick/" + playerId, { method: "POST" })
                    .then(res => res.json())
                    .then(data => {
                        if (data.error) alert(data.error);
                        else pollStatus();
                    })
                    .catch(err => console.error("Kick error:", err));
            });
        });
    }
    bindKickButtons();

    function bindReadyButtons() {
        document.querySelectorAll(".ready-btn").forEach(btn => {
            btn.addEventListener("click", function () {
                btn.disabled = true;
                fetch(API_BASE + "/ready", { method: "POST" })
                    .then(res => res.json())
                    .then(data => {
                        if (!data.error) {
                            resetPollRate();
                            pollStatus();
                        }
                    })
                    .catch(err => console.error("Ready toggle error:", err))
                    .finally(() => {
                        setTimeout(() => { btn.disabled = false; }, 1500);
                    });
            });
        });
    }
    bindReadyButtons();

    if (leaveBtn) {
        leaveBtn.addEventListener("click", () => {
            if (!confirm("Leave this lobby?")) return;

            fetch(API_BASE + "/leave", { method: "POST" })
                .then(res => res.json())
                .then(data => {
                    if (data.error) alert(data.error);
                    else window.location.href = "/lobbies";
                })
                .catch(err => console.error("Leave error:", err));
        });
    }

    if (abandonBtn) {
        abandonBtn.addEventListener("click", () => {
            if (!confirm("Abandon this lobby? This will permanently shut it down and all uploaded files will be lost. This cannot be undone.")) return;

            fetch(API_BASE + "/close", { method: "POST" })
                .then(res => res.json())
                .then(data => {
                    if (data.error) alert(data.error);
                    else window.location.href = "/lobbies";
                })
                .catch(err => console.error("Abandon error:", err));
        });
    }

    if (lockBtn) {
        lockBtn.addEventListener("click", () => {
            const isLocking = currentState === LOBBY_STATE_OPEN;
            const msg = isLocking
                ? "Lock this lobby? New players will no longer be able to join."
                : "Unlock this lobby? New players will be able to join again.";
            if (!confirm(msg)) return;

            fetch(API_BASE + "/lock", { method: "POST" })
                .then(res => res.json())
                .then(data => {
                    if (data.error) alert(data.error);
                    else { resetPollRate(); pollStatus(); }
                })
                .catch(err => console.error("Lock error:", err));
        });
    }

    if (generateBtn) {
        generateBtn.addEventListener("click", () => {
            if (lastReadyCount < lastTotalCount) {
                const unready = lastTotalCount - lastReadyCount;
                if (!confirm(`${unready} player(s) are not ready yet. Generate anyway?`)) return;
            } else {
                if (!confirm("Generate the seed with all uploaded YAMLs?")) return;
            }

            generateBtn.disabled = true;
            generateBtn.textContent = "Generating...";

            fetch(API_BASE + "/generate", { method: "POST" })
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        alert("Generation error: " + data.error);
                        generateBtn.disabled = false;
                        generateBtn.textContent = "Generate Seed";
                    } else {
                        resetPollRate();
                        pollStatus();
                    }
                })
                .catch(err => {
                    console.error("Generate error:", err);
                    generateBtn.disabled = false;
                    generateBtn.textContent = "Generate Seed";
                });
        });
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.appendChild(document.createTextNode(text));
        return div.innerHTML;
    }

    const settingsModal = document.getElementById("settings-modal");
    const settingsSaveBtn = document.getElementById("settings-save-btn");
    const settingsCancelBtn = document.getElementById("settings-cancel-btn");

    function openSettingsModal() {
        if (settingsModal) settingsModal.classList.add("open");
    }

    function closeSettingsModal() {
        if (settingsModal) settingsModal.classList.remove("open");
    }

    if (settingsEditBtn) {
        settingsEditBtn.addEventListener("click", openSettingsModal);
    }
    if (settingsCancelBtn) {
        settingsCancelBtn.addEventListener("click", closeSettingsModal);
    }
    if (settingsModal) {
        settingsModal.addEventListener("click", e => {
            if (e.target === settingsModal) closeSettingsModal();
        });
    }
    if (settingsSaveBtn) {
        settingsSaveBtn.addEventListener("click", () => {
            const maxPlayersEl = document.getElementById("edit-max-players");
            const newMaxYamls = parseInt(document.getElementById("edit-max-yamls").value);
            if (newMaxYamls < maxYamlsHeld) {
                alert(`Cannot lower max YAMLs below ${maxYamlsHeld} — a player already has that many.`);
                return;
            }

            const allowCustomEl = document.getElementById("edit-allow-custom-apworlds");
            const payload = {
                title: document.getElementById("edit-title").value.trim(),
                max_yamls_per_player: newMaxYamls,
                timeout_minutes: parseInt(document.getElementById("edit-timeout").value),
                max_players: maxPlayersEl ? parseInt(maxPlayersEl.value) || 0 : undefined,
                release_mode: document.getElementById("edit-release-mode").value,
                collect_mode: document.getElementById("edit-collect-mode").value,
                remaining_mode: document.getElementById("edit-remaining-mode").value,
                countdown_mode: document.getElementById("edit-countdown-mode").value,
                hint_mode: document.getElementById("edit-hint-mode").value,
                hint_cost: parseInt(document.getElementById("edit-hint-cost").value),
                item_cheat: document.getElementById("edit-item-cheat").value === "1",
                spoiler: parseInt(document.getElementById("edit-spoiler").value),
                allow_custom_apworlds: allowCustomEl ? allowCustomEl.checked : undefined,
            };

            settingsSaveBtn.disabled = true;
            settingsSaveBtn.textContent = "Saving…";

            fetch(API_BASE + "/settings", {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            })
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        alert("Error: " + data.error);
                        settingsSaveBtn.disabled = false;
                        settingsSaveBtn.textContent = "Save";
                    } else {
                        location.reload();
                    }
                })
                .catch(err => {
                    console.error("Settings error:", err);
                    settingsSaveBtn.disabled = false;
                    settingsSaveBtn.textContent = "Save";
                });
        });
    }

    if (generateStandard && generateCustom) {
        const isCustomMode = hasCustomYamls && (currentState === LOBBY_STATE_OPEN || currentState === LOBBY_STATE_LOCKED);
        generateStandard.style.display = isCustomMode ? "none" : "";
        generateCustom.style.display = isCustomMode ? "" : "none";
    }

    // Set initial expiry display from server-rendered values
    (function () {
        const expiryEl = document.getElementById("lobby-expiry");
        if (expiryEl && typeof LOBBY_LAST_ACTIVITY !== "undefined" && typeof TIMEOUT_MINUTES !== "undefined") {
            const expiryMs = new Date(LOBBY_LAST_ACTIVITY).getTime() + TIMEOUT_MINUTES * 60000;
            expiryEl.textContent = "Expires: " + new Date(expiryMs).toLocaleString();
        }
    })();

    document.querySelectorAll(".chat-time[data-utc]").forEach(el => {
        el.textContent = new Date(el.dataset.utc).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });

    // YAML viewer modal
    const yamlViewModal = document.getElementById("yaml-view-modal");
    const yamlViewClose = document.getElementById("yaml-view-close");
    const yamlViewFilename = document.getElementById("yaml-view-filename");
    const yamlViewBody = document.getElementById("yaml-view-body");

    function openYamlViewModal(yamlId, filename) {
        fetch(`${API_BASE}/yaml/${yamlId}?view=1`)
            .then(res => {
                if (!res.ok) throw new Error("Failed to load YAML");
                return res.text();
            })
            .then(text => {
                if (yamlViewFilename) yamlViewFilename.textContent = filename;
                if (yamlViewBody) yamlViewBody.textContent = text;
                if (yamlViewModal) yamlViewModal.classList.add("open");
            })
            .catch(err => {
                console.error("YAML view error:", err);
                alert("Could not load YAML content.");
            });
    }

    function closeYamlViewModal() {
        if (yamlViewModal) yamlViewModal.classList.remove("open");
    }

    if (yamlViewClose) {
        yamlViewClose.addEventListener("click", closeYamlViewModal);
    }
    if (yamlViewModal) {
        yamlViewModal.addEventListener("click", e => {
            if (e.target === yamlViewModal) closeYamlViewModal();
        });
    }

    function bindYamlViewButtons() {
        document.querySelectorAll(".yaml-view-btn").forEach(btn => {
            btn.addEventListener("click", function () {
                openYamlViewModal(this.dataset.yamlId, this.dataset.filename);
            });
        });
    }
    bindYamlViewButtons();

    pollStatus();
    pollTimer = setInterval(pingAndMaybePoll, pollInterval);
})();
