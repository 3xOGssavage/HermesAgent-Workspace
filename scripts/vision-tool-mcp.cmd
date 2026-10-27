@echo off
REM Vision-tool MCP wrapper: runs from its own folder so its
REM helper modules import correctly. Backend key (Gemini) comes
REM from the Hermes secrets file, never written here.
cd /d F:\CD\Hermes Agent\scripts\vision-tool || exit /b 1
python vision_mcp_server.py
