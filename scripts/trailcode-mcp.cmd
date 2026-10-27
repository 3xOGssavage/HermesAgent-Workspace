@echo off
REM TrailCode MCP wrapper for Hermes's own map (Neohelper side).
REM Pinned to 0.15.0: newer 0.25.x serves deferred tools that this
REM client cannot consume (tools/list returns empty).
cd /d F:\CD\Hermes Agent || exit /b 1
CALL "C:\Users\user\AppData\Roaming\npm\graft.cmd" mcp "F:\CD\Hermes Agent"
