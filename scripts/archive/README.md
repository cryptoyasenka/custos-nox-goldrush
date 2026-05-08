# scripts/archive — старые генераторы (до 2026-05-08)

**Перенесено 2026-05-08.** Старый Python+ffmpeg pipeline для генерации видео и слайдов.

## Что в архиве

- `gen_f2_video.py`, `gen_f2_v2.py` — Python pipeline для F2 (выходы в `assets/archive/`)
- `gen_f3_video.py` — F3 pipeline (вывод `assets/archive/f3-demo.mp4`)
- `gen_pitch_slides.py` — генератор PNG слайдов (заменён HTML deck-v2.html)

## Что взамен

- F2: Playwright + edge-tts + CapCut. См. `video-build/f2/record-slides-individual.mjs`
  и `planning/VIDEO-2-PITCH.txt`.
- F3: Live запись + architecture overlay. См. `planning/VIDEO-3-DEMO.txt`.
- Slides: HTML 8-слайдный deck `assets/pitch-slides/deck-v2.html`.
