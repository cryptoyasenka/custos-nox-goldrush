# assets/archive — старые финальные видео + temp dirs (до 2026-05-08)

**Перенесено 2026-05-08** при чистке от старого F2 pipeline.

## Старые финальные mp4 (выходы старого Python+ffmpeg pipeline)

- `f2-pitch.mp4` (May 5) — F2 v1
- `f2-pitch-v2.mp4` (May 5) — F2 v2
- `f2-pitch-final.mp4` (May 5) — F2 final (старого подхода)
- `f3-demo.mp4` (May 5) — F3 demo (старого подхода)
- `Generated Audio May 05, 2026 - 7_50PM.wav` — VO эксперимент

## pitch-slides-old/

PNG-слайды + старый HTML deck — **заменены на `assets/pitch-slides/deck-v2.html`**
(8 интерактивных HTML-слайдов вместо 7 PNG):
- `deck.html` — v1 деки
- `pitch-slide-{01..07}.png` — слайды от April 30 (commit `0557dee`)

## temp-dirs/

Промежуточные папки от Python генераторов (`scripts/archive/gen_f2_*.py`):
- `_f2_tmp/`, `_f2v2_tmp/`, `_f3_tmp/`
- `_slides_preview/`, `_promo_frames/`

Игнорируются в `.gitignore`. Можно безопасно удалить.

## Что взамен (текущий pipeline)

См. `assets/pitch-slides/deck-v2.html` + `video-build/f2/record-slides-individual.mjs`.
Подробности в `video-build/f2/archive/README.md`.
