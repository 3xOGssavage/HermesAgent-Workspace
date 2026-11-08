# VoiceStudio local control (loopback MCP + REST, Nov 2026)

Speak to the app only while its window is open. Base: `http://localhost:3900`.
Health: `GET /health` returns status/device/version. TTS: `POST /v1/audio/speech`
(OpenAI shape: model/input/voice) writes the audio file directly.

## MCP session handshake (streamable HTTP — plain curl works)

Every call needs BOTH headers or the server rejects it:
`Content-Type: application/json` + `Accept: application/json, text/event-stream`.
Responses arrive as SSE (`data: {...}` lines — parse the JSON after `data:`).

1. `POST /mcp` body `{"jsonrpc":"2.0","id":1,"method":"initialize",
   "params":{"protocolVersion":"2024-11-05","capabilities":{},
   "clientInfo":{"name":"...","version":"..."}}}`.
2. Read the `mcp-session-id` RESPONSE HEADER (not the body) and send it
   as the `mcp-session-id` header on every later call.
3. `POST /mcp` `notifications/initialized` (no params), then
   `tools/list`, then `tools/call` with
   `{"name":"<tool>","arguments":{...}}`.
4. A fresh app restart invalidates the session id — re-handshake.

## TTS engine routing (the part that bites)

- MCP `generate_speech` takes `text`, optional `profile_id`, `language`,
  `speed`, `steps`, `format` — it has NO engine parameter and always
  follows the app's ACTIVE engine. To change engines, switch first:
  `POST /engines/select` body `{"family":"tts","backend_id":"voxcpm2"}`,
  or pick REST `model:"voxcpm2"` per request. REST `model:"tts-1"`
  follows whatever is active — never assume which engine that is.
- A `403 .../generate` after a model deletion means the backend still
  routes to the deleted weights: restart the app so it re-resolves, then
  re-select the engine. A `model_licence_required` naming a repo means
  that repo's license was never accepted in the Model Catalogue.
- After deleting a license-blocked model, never run the app's Fix-all /
  full-setup again unchecked: it re-downloads factory defaults INCLUDING
  the blocked weights. Install only green-badge engines one by one.

## License purge procedure (all Models sub-pages, not just TTS)

1. Open every sub-page (TTS, ASR, Dictation, Diarisation, Translation,
   LLM) and read each row's badge: green = permissive, keep; red icon or
   orange `Accept licence to use` = blocked, delete its weights from disk.
2. Rows offering only Download/Install were never fetched — nothing to
   remove, just never install them.
3. Deleting weights breaks the feature that used them (dictation voices,
   a translator): confirm the pipeline never calls that feature first
   (ours uses whisperX, Argos stays), then delete and restart the app
   so its lists stop showing ghosts.
