from __future__ import annotations

'''Stubbing worlds/AutoSNIClient and SNIClient.py because it should be in worlds/_sni to match _bizhawk'''

__all__ = ["AutoSNIClientRegister", "SNIClient", "SnesReader", "SnesData", "valid_patch_suffix", "Read"]

from worlds._sni.client import AutoSNIClientRegister, SNIClient, SnesReader, SnesData, Read, valid_patch_suffix
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components

component = Component('SNI Client', 'SNIClient', component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apsoe"),
                      description="A client for connecting to SNES consoles via Super Nintendo Interface.")
components.append(component)
