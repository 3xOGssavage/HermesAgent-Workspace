@echo off
REM Graft MCP wrapper: the graft server resolves its repo from the
REM working folder, so run it from the indexed repo (Neocoder keeps
REM F:\CD\Opencode\graft\ fresh). Hermes has no git repo of its own.
REM Points at Neocoder's main project (neodev-portal), the folder
REM with the real prebuilt map. The Opencode root has no map of
REM its own. Pinned to 0.15.0: newer 0.25.x serves deferred tools
REM that this client cannot consume (tools/list returns empty).
cd /d F:\CD\Opencode\Projects\neodev-portal || exit /b 1
CALL "C:\Users\user\AppData\Roaming\npm\graft.cmd" mcp "F:\CD\Opencode\Projects\neodev-portal"
