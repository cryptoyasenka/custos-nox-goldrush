"""
F2 Pitch Video generator - edge-tts voiceover + slide images -> MP4
Output: assets/f2-pitch.mp4 (~1:56)
"""
import asyncio, subprocess, os, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
SLIDES_DIR = ROOT / "assets" / "pitch-slides"
OUT_DIR = ROOT / "assets"
TMP = ROOT / "assets" / "_f2_tmp"
TMP.mkdir(exist_ok=True)

VOICE = "en-US-AriaNeural"

# Script per slide — exact text from PITCH-SCRIPT-F2.md
SEGMENTS = [
    {
        "slide": "pitch-slide-01.png",
        "text": (
            "On April 1st, 2026, 285 million dollars drained from Drift Protocol — "
            "more than half of TVL. "
            "The attack didn't happen in one transaction. It took weeks. "
            "A migrated Security Council multisig with a 2-of-5 threshold and zero timelock. "
            "Durable nonces seeded by privileged signers. "
            "A pre-signed admin transfer waiting in the queue. "
            "Every step happened on chain. In public. Nobody noticed."
        ),
    },
    {
        "slide": "pitch-slide-02.png",
        "text": (
            "Solana Foundation's STRIDE monitors protocols with 10 million or more in TVL. "
            "Maybe a hundred projects. "
            "There are thousands of DAOs, grant committees, and treasury multisigs below that line. "
            "They have nothing."
        ),
    },
    {
        "slide": "pitch-slide-03.png",
        "text": (
            "Custos Nox is an open-source daemon. "
            "It watches Solana accounts over Helius WebSocket and fires an alert "
            "when a config change matches an attack pattern. "
            "Five detectors live today. "
            "Four map to the Drift attack chain — timelock removed, multisig weakened, "
            "nonce seeded, stale nonce executed. "
            "The fifth catches signer rotation. "
            "Any single alert would have stopped the drain."
        ),
    },
    {
        "slide": "pitch-slide-04.png",
        "text": (
            "The repo is public. 205 tests, GitHub Actions green. "
            "A devnet smoke harness replays three Drift attack steps plus signer rotation — "
            "four live alerts under a second each. "
            "Live dashboard at custos-nox dot up dot railway dot app."
        ),
    },
    {
        "slide": "pitch-slide-05.png",
        "text": (
            "First users: Squads multisig operators — protocol treasuries, grant committees, "
            "hackathon prize pools. They're already on Discord. "
            "Integration is one webhook URL and a five-minute self-host. "
            "MIT licensed, no paid tiers. "
            "Issue tracker is open for detector requests."
        ),
    },
    {
        "slide": "pitch-slide-06.png",
        "text": (
            "Long term: a hosted feed that any DAO subscribes to with zero infra. "
            "Top-50 Solana multisigs pre-watched. "
            "The security layer between on-chain governance and the first Discord alert."
        ),
    },
    {
        "slide": "pitch-slide-07.png",
        "text": (
            "I'm Yasya from Superteam Ukraine. "
            "Code is live on GitHub, demo runs on devnet, five detectors are watching right now. "
            "github dot com slash cryptoyasenka slash custos dash nox."
        ),
    },
]

async def gen_audio(text: str, out_path: Path):
    import edge_tts
    communicate = edge_tts.Communicate(text, VOICE, rate="+8%")
    await communicate.save(str(out_path))

def get_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", str(path)],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return float(data["streams"][0]["duration"])

def make_segment_video(slide_path: Path, audio_path: Path, out_path: Path, duration: float):
    """Slide image + audio → short MP4 segment with 0.3s fade in/out"""
    fade_dur = 0.3
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(slide_path),
        "-i", str(audio_path),
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "128k",
        "-vf", f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,"
               f"fade=t=in:st=0:d={fade_dur},fade=t=out:st={duration-fade_dur}:d={fade_dur}",
        "-af", f"afade=t=in:st=0:d={fade_dur},afade=t=out:st={duration-fade_dur}:d={fade_dur}",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(out_path)
    ], check=True, capture_output=True)

async def main():
    segment_files = []

    for i, seg in enumerate(SEGMENTS):
        print(f"[{i+1}/{len(SEGMENTS)}] {seg['slide']} ...")
        audio_path = TMP / f"seg_{i:02d}.mp3"
        video_path = TMP / f"seg_{i:02d}.mp4"
        slide_path = SLIDES_DIR / seg["slide"]

        # Generate TTS
        await gen_audio(seg["text"], audio_path)

        # Get audio duration
        duration = get_duration(audio_path)
        print(f"  duration: {duration:.1f}s")

        # Render segment
        make_segment_video(slide_path, audio_path, video_path, duration)
        segment_files.append(video_path)

    # Write concat list
    concat_list = TMP / "concat.txt"
    with open(concat_list, "w") as f:
        for vf in segment_files:
            f.write(f"file '{vf.as_posix()}'\n")

    # Final concat
    out_path = OUT_DIR / "f2-pitch.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(out_path)
    ], check=True)

    duration = get_duration(out_path)
    print(f"\nDONE F2: {out_path}")
    print(f"   Total duration: {duration:.1f}s ({duration/60:.1f} min)")
    print(f"   File size: {out_path.stat().st_size / 1024 / 1024:.1f} MB")

asyncio.run(main())
