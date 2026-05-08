# video-build/f2/archive — старый F2 pipeline (до 2026-05-08)

Это **deprecated** артефакты от модульного `hook + terminal + outro` подхода
(коммиты до `c13c15a`). НЕ использовать для новой записи.

## Что заменило этот pipeline

Новый F2 pipeline (с 2026-05-08, коммит `c13c15a`):
- 8-слайдный HTML deck → `assets/pitch-slides/deck-v2.html`
- Veo3 intro clip → `assets/Blockchain_transactions_flow_red…_202605081236.mp4`
- Per-slide Playwright recorder → `video-build/f2/record-slides-individual.mjs`
- Output: `video-build/f2/slides-individual/slide-{1..8}.webm` для CapCut
- Voice: edge-tts по `planning/PITCH-SCRIPT-F2.md`

## Что в этой папке

**Recorders/builders** (модульный подход):
- `record-html.mjs`, `record-cover.mjs`, `record-howworks.mjs`
- `build-f2.sh` — concat hook + terminal + outro + VO через ffmpeg
- `gen-vo.sh` — 22-chunk edge-tts по старому 22-фразному narrative
- `prepare-terminal.sh`, `TERMINAL-RUNBOOK-F2.md` — single-detector terminal recording

**HTML/webm куски** (заменены на 8 слайдов в deck-v2):
- `hook.html` / `hook.webm` — cinematic opener (теперь Veo3 intro + slide 1)
- `outro.html` / `outro.webm` — старая аутро (теперь slide 8)
- `cover.html` / `cover.webm` — обложка (теперь slide 1)
- `howworks.html` / `howworks.webm` — объяснялка (теперь slide 5)
- `slides.html` — старый агрегат (заменён `deck-v2.html`)

**Старые финальные mp4 + VO mp3:**
- `terminal-f2.mp4`, `final-f2.mp4` (May 5)
- `vo-f2.mp3`, `vo-f2-final.mp3`, `vo-f2.ssml`
- `test-ssml.mp3`, `test2.mp3`, `test3.mp3` — sample эксперименты edge-tts
- `chunks/` — 22 chunk MP3 для старого VO

**Кадры/jpg от старого pipeline:**
- `hook-frame-{10s,20s}.jpg`, `existing-{2s,20s,55s,90s}.jpg`

## Если нужно вернуть к старому pipeline

```bash
git log --oneline c13c15a^..bbb5e28 -- video-build/f2/
```

Но будь готова, что narrative будет 22-chunk Drift-forensics scenarii, а не 8-слайдный deck.
