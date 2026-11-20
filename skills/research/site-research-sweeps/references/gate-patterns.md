# Gate patterns (reusable diagnosis playbook)

Match the symptom, run the sequence, log the verdict. All patterns below recurred across batches.

| Symptom | Likely cause | Sequence | Verdict to log |
|---|---|---|---|
| `cover: stuck` all views, loader visible in stuck shot | Asset-gated intro or sound/entry gate | Vision stuck shot -> handpass (persistent ctx) -> click probe -> precedent NOTES | `gate-blocked`, skip redundant views per compounding rule |
| Enter button unfound by text matcher (`candidates= 0`) | Control is div-handled or shares node with icon | Bounding-box click, else coordinate fallback (bottom-center); verify entry with vision | `entered via fallback click`; note finder caveat |
| `scrollH = viewport`, no cover, glide skipped | Virtual-scroll canvas world | `wheel-drive.mjs` (small shoves); confirm movement with vision on mid-drive still | `virtual+wheel`; drive logs as proof |
| Stuck covers after successes an hour earlier | Fresh-load throttling, not a real gate | Handpass check; if handpass enters, resume captures with gaps | `throttled, resumed` |
| Loader spins through full handpass + click probe | Intro never resolves in automation | Log as hang; carry prior-batch settled-state patterns as explicitly unverified | `loader-hang`, hover/scroll claims marked prior-only |
| Wheel shoves do not change scenes | Hotspot/click-gated progression, not scroll | Screenshot the prompt UI; one targeted click-probe max, then log unconfirmed | `hotspot-gated`, next beat unconfirmed |
| Glide segments all `y=0` with no quartile marks on a tall page, consent banner visible in hero shot | Consent overlay intercepting scroll until choice | Handpass (auto-accepts banners) to confirm, then re-run rig | `consent-gated`, rig re-run after accept |
| Gate renders fully but clicks never enter after probe + long settle | Canvas overlay swallowing clicks or dead event wiring (common on old sites) | Finder-probe the control's box, coordinate-click it, one long-settle retry max, vision-verify | `gate-stall`; journey carried as prior |
| Wheel advances desktop but phone stays on landing after tap+wheel | Touch-scroll world ignores wheel events; drag is the input | One CDP `dispatchTouchEvent` drag probe (entry tap, 2 swipes, screenshot each); if beats change, phone needs drag not wheel | `drag-only-mobile`, phone flight via drag probe |
| A canvas-gate coordinate verified on desktop misses on phone | Gate layout fractions differ by breakpoint, and `mouse.click` silently misses on touch contexts | Re-verify the tap point per platform (never scale one fraction across breakpoints); mobile contexts get `touchscreen.tap`, desktop gets `mouse.click` — carry both in the driver | `entered <platform> via tap|click @fraction` |
| Wheel never leaves the top on any view while a modal/overlay is visible | Overlay traps scroll though the page behind is fine | Dismiss (Escape/X) in a probe, vision-verify the hero clean, then re-drive; keep pre-dismiss flights labeled as trap evidence, not journey evidence. If the trap RETURNS mid-drive (modal reappears after the initial dismiss — verify with a late still, not the 000 shot), add periodic Escape presses inside the wheel loop (e.g. every 16 shoves) in the per-site driver rather than re-running the same single-dismiss drive | `modal-trap`, post-dismiss flight is the evidence; `modal-trap returns` when timing drifts |
| Screenshots change across runs with no input to explain it | Attract/idle loop cycling beats, not travel | Timed screenshots with zero input (3x ~20s apart); beats changing unprompted means it loops — wheel position and shown beat do not map 1:1 | `attract-loop`, journey claims require input-correlated change |
| Prior batch says gate/block/no-menu and the fresh capture contradicts it | Sites drift: walls lift, menus appear, inline nav collapses | Treat prior-batch verdicts as hypotheses; re-verify headline claims on fresh evidence before inheriting or overturning them | `drift verified <claim>`, delta logged |
| `cover: stuck` on every retry but the stuck shot shows a fully rendered hero with no loader | Probe selector matches a persistent on-page element, not a loader — further retries only burn time | Stop after one vision-verified misfire; handpass becomes the primary evidence; skip remaining views under compounding | `cover-misfire`, rig views logged as skipped |
| All glide segs read `y=0` on a tall page on first load, then bottom on immediate retry | First-load GPU/contention jack, not a real gate | Retry the view unchanged once before diagnosing | `first-load jack, warm retry wins` |
| Glide segs stall at the identical y across views while the page is far taller | Pinned/sticky section or scroll-trap holding scroll | Vision-check the stall point for the pinning content; log capped-at-y with the cause, never as failure | `sticky-capped`, content at stall verified |

Finder notes:

- Exact-text matchers fail when a label shares its node with an icon — prefer contains-match plus bounding-box click.
- When the matcher finds zero candidates, DOM-probe clickable texts plus bounding boxes first (`button, a, [role=button]` matching /enter|begin|start|continue/i), then click the real coordinates — one probe run is cheaper than repeated blind coordinate guesses.
- Zero console errors does NOT mean loaded — silent hangs are real; vision is the arbiter.
- A fallback-named glide video with `skipped: true` in its fingerprint is not a glide — never claim `glideBottom` from filenames.
