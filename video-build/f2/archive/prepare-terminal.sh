#!/usr/bin/env bash
# prepare-terminal.sh — нарезает два MKV и склеивает в terminal-f2.mp4
#
# test clip:     trim 2s start / 5s end  + заморозка "205 passed" 12s
# terminal clip: trim 4s start / 7s end  + заморозка CRITICAL 22s
# итого: ~76s
set -e

VIDEOS="C:/Users/Yana/Videos"
TEST_MKV="$VIDEOS/2026-05-05 18-31-34.mkv"
TERM_MKV="$VIDEOS/2026-05-05 18-10-06.mkv"

for f in "$TEST_MKV" "$TERM_MKV"; do
  [ -f "$f" ] || { echo "✗ не найден: $f"; exit 1; }
done

echo "→ Test clip (trim + freeze 12s на '205 passed')..."
# 22.9s - 5s end = 17.9s
ffmpeg -y -ss 2 -to 17.9 -i "$TEST_MKV" \
  -vf "tpad=stop_mode=clone:stop_duration=12" \
  -c:v libx264 -preset fast -pix_fmt yuv420p -crf 22 -an \
  test-trimmed.mp4 -loglevel quiet
echo "  $(ffprobe -v quiet -show_entries format=duration -of csv=p=0 test-trimmed.mp4)s"

echo "→ Terminal clip (trim 4s / 7s + freeze 22s на CRITICAL)..."
# 36.4s - 7s end = 29.4s
ffmpeg -y -ss 4 -to 29.4 -i "$TERM_MKV" \
  -vf "tpad=stop_mode=clone:stop_duration=22" \
  -c:v libx264 -preset fast -pix_fmt yuv420p -crf 22 -an \
  terminal-trimmed.mp4 -loglevel quiet
echo "  $(ffprobe -v quiet -show_entries format=duration -of csv=p=0 terminal-trimmed.mp4)s"

echo "→ Склейка..."
printf "file 'test-trimmed.mp4'\nfile 'terminal-trimmed.mp4'\n" > terminal-concat.txt
ffmpeg -y -f concat -safe 0 -i terminal-concat.txt \
  -c copy terminal-f2.mp4 -loglevel quiet

DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 terminal-f2.mp4)
echo ""
echo "✓ terminal-f2.mp4 готов — ${DUR}s"
echo "  Следующий шаг: bash build-f2.sh"

rm -f test-trimmed.mp4 terminal-trimmed.mp4 terminal-concat.txt
