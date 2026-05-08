"""
F2 Pitch Video v2 — high-quality rebuild
Improvements over v1:
  - Terminal animation clip replaces static slide 04 (live proof the tool works)
  - Ken Burns slow zoom on every static slide (1.0 -> 1.12x, 30fps)
  - Crossfade dissolve transitions (xfade video + acrossfade audio)
  - Improved slides 05 and 06 (stronger copy, bigger text)
Output: assets/f2-pitch-v2.mp4
"""
import asyncio, subprocess, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT     = Path(__file__).resolve().parents[1]
SLIDES   = ROOT / "assets" / "pitch-slides"
OUT_DIR  = ROOT / "assets"
TMP      = ROOT / "assets" / "_f2v2_tmp"
TMP.mkdir(parents=True, exist_ok=True)

VOICE      = "en-US-AriaNeural"
XFADE_DUR  = 0.45   # crossfade overlap in seconds
ZOOM_SPEED = 0.0006  # Ken Burns: zoom increment per frame
ZOOM_MAX   = 1.12   # Ken Burns: maximum zoom
FPS        = 30

W, H = 1920, 1080

# ── Brand palette (slide theme) ───────────────────────────────────────────────
BG_S     = (10, 10, 10)
FG_S     = (237, 237, 237)
MUTED_S  = (113, 113, 122)
DIM_S    = (82, 82, 91)
DIV_S    = (39, 39, 42)
GREEN_S  = (74, 222, 128)
CYAN_S   = (103, 232, 249)
ORANGE_S = (251, 146, 60)

# ── Terminal palette (GitHub dark) ────────────────────────────────────────────
BG_T  = "#0d1117"
FG_T  = "#c9d1d9"
GRN_T = "#3fb950"
RED_T = "#ff6b6b"
ORG_T = "#f0883e"
BLU_T = "#58a6ff"
GRY_T = "#8b949e"

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── Font helpers ──────────────────────────────────────────────────────────────
def sfont(name, size):
    return ImageFont.truetype(name, size)

F_BLACK = lambda s: sfont("seguibl.ttf", s)
F_BOLD  = lambda s: sfont("segoeuib.ttf", s)
F_SEMI  = lambda s: sfont("seguisb.ttf", s)
F_REG   = lambda s: sfont("segoeui.ttf", s)

def tfont(size=20, bold=False):
    try:
        return ImageFont.truetype("consolab.ttf" if bold else "consola.ttf", size)
    except Exception:
        return ImageFont.load_default()

# ── Slide helpers ─────────────────────────────────────────────────────────────
def new_slide():
    img = Image.new("RGB", (W, H), BG_S)
    return img, ImageDraw.Draw(img)

def chrome(img, draw, slide_no, total=7):
    logo = Image.open(ROOT / "assets" / "logo.png").convert("RGBA")
    logo_s = logo.resize((48, 48), Image.LANCZOS)
    img.paste(logo_s, (60, 50), logo_s)
    draw.text((120, 56), "CUSTOS NOX", font=F_BOLD(28), fill=FG_S)
    sub = "F2 PITCH"
    sw = draw.textlength(sub, font=F_SEMI(20))
    draw.text((W - 60 - sw, 60), sub, font=F_SEMI(20), fill=MUTED_S)
    draw.line([(60, 110), (W - 60, 110)], fill=DIV_S, width=1)
    draw.line([(60, H - 90), (W - 60, H - 90)], fill=DIV_S, width=1)
    draw.text((60, H - 60), f"{slide_no:02d} / {total:02d}", font=F_SEMI(20), fill=MUTED_S)
    meta = "Frontier 2026  ·  Superteam Ukraine"
    mw = draw.textlength(meta, font=F_SEMI(20))
    draw.text((W - 60 - mw, H - 60), meta, font=F_SEMI(20), fill=MUTED_S)

def center(draw, text, fnt, y, fill=None):
    fill = fill or FG_S
    tw = draw.textlength(text, font=fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

# ── Improved slides (generated to TMP, not overwriting originals) ─────────────
def make_slide_05():
    """WHO USES THIS — stronger third bullet: MIT licensed, no paid tiers."""
    img, d = new_slide()
    chrome(img, d, 5)
    center(d, "WHO USES THIS", F_SEMI(36), 220, MUTED_S)
    center(d, "First users:", F_BOLD(64), 295, FG_S)
    center(d, "Squads multisig operators", F_BLACK(96), 385, CYAN_S)
    center(d, "protocol treasuries  ·  grant committees  ·  hackathon prize pools",
           F_REG(36), 515, MUTED_S)
    bullets = [
        ("1 webhook URL",           FG_S),
        ("5-minute self-host",      FG_S),
        ("MIT licensed  ·  no paid tiers", GREEN_S),
    ]
    y = 665
    for text, color in bullets:
        center(d, text, F_SEMI(48), y, color)
        y += 84
    p = TMP / "slide-05-v2.png"
    img.save(p)
    return p

def make_slide_06():
    """VISION — two punchy lines instead of four small gray ones."""
    img, d = new_slide()
    chrome(img, d, 6)
    center(d, "VISION", F_SEMI(36), 225, MUTED_S)
    center(d, "Hosted feed", F_BLACK(108), 295, FG_S)
    center(d, "Zero-infra monitoring", F_BLACK(108), 425, CYAN_S)
    center(d, "Top-50 Solana multisigs — pre-watched", F_SEMI(44), 650, FG_S)
    center(d, "Any DAO. One click. Discord ping. Done.", F_BOLD(52), 728, ORANGE_S)
    p = TMP / "slide-06-v2.png"
    img.save(p)
    return p

# ── Terminal animation data ───────────────────────────────────────────────────
MULTISIG = "Chst4kw6UkFiDo6eEDUcrpXSoLg2p6BdZAYCcE5Pxg7z"

DAEMON_LINES = [
    ("> npm run dev", BLU_T),
    "",
    ("[custos] cluster=devnet", GRY_T),
    ("[custos] rpc=https://api.devnet.solana.com", GRY_T),
    ("[custos] detectors loaded: 5", GRN_T),
    ("[custos] subscribe account=" + MULTISIG[:30] + "...", GRY_T),
    ("[custos] baseline seeded. watching.", GRN_T),
    "",
]

ALERT_LINES = [
    ("CRITICAL [squads-timelock-removal]",         RED_T),
    ("  Timelock removed on multisig",              FG_T),
    ("  " + MULTISIG,                              GRY_T),
    ("  link: solscan.io/account/Chst4k...?cluster=devnet", BLU_T),
    ('  ctx:  {"reason":"timelock_reduced",',       GRY_T),
    ('         "previousTimelockSeconds":86400,',   GRY_T),
    ('         "currentTimelockSeconds":0}',        GRY_T),
]

LEFT_BLANK = [("C:\\Projects\\custos> ", FG_T)]
LEFT_CMD   = [
    ("C:\\Projects\\custos> npm run smoke:timelock \\", BLU_T),
    ("    -- " + MULTISIG[:22] + "...", BLU_T),
    "",
]
LEFT_DONE  = LEFT_CMD + [("  tx confirmed: 5Jwth...batD", GRY_T), ""]

def render_terminal(left_lines, right_lines):
    img  = Image.new("RGB", (W, H), hex2rgb(BG_T))
    draw = ImageDraw.Draw(img)
    font  = tfont(20)
    titf  = tfont(17)
    mid   = W // 2

    draw.line([(mid, 0), (mid, H)], fill=hex2rgb(GRY_T), width=1)
    draw.rectangle([0, 0, mid - 1, 32],  fill=hex2rgb("#161b22"))
    draw.rectangle([mid + 1, 0, W, 32],  fill=hex2rgb("#161b22"))
    draw.text((16,      8), "Terminal 1 — attacker",      font=titf, fill=hex2rgb(GRY_T))
    draw.text((mid + 16, 8), "Terminal 2 — custos daemon", font=titf, fill=hex2rgb(GRY_T))

    def render_side(lines, x0):
        y, lh = 48, 27
        for line in lines:
            text, color = (line, FG_T) if isinstance(line, str) else line
            draw.text((x0, y), text, font=font, fill=hex2rgb(color))
            y += lh

    render_side(left_lines,       16)
    render_side(right_lines, mid + 16)
    return img

def build_term_frames():
    """Returns [(PIL_image, duration_sec | None)] — last frame duration filled in later."""
    frames = []
    # daemon ready, cursor blinking on left
    frames.append((render_terminal(LEFT_BLANK, DAEMON_LINES), 1.0))
    # command appears
    frames.append((render_terminal(LEFT_CMD,   DAEMON_LINES), 0.7))
    # tx confirmed
    frames.append((render_terminal(LEFT_DONE,  DAEMON_LINES), 0.5))
    # alert lines appear one by one
    timings = [0.6, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45]
    alert_so_far = []
    for line, dur in zip(ALERT_LINES, timings):
        alert_so_far.append(line)
        frames.append((render_terminal(LEFT_DONE, DAEMON_LINES + alert_so_far), dur))
    # final hold — duration computed from TTS length
    frames.append((render_terminal(LEFT_DONE, DAEMON_LINES + ALERT_LINES), None))
    return frames

# ── ffmpeg helpers ────────────────────────────────────────────────────────────
async def gen_audio(text, path):
    import edge_tts
    comm = edge_tts.Communicate(text, VOICE, rate="+8%")
    await comm.save(str(path))

def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(r.stdout)["streams"][0]["duration"])

def make_slide_segment(slide_path, audio_path, out_path, duration):
    """Static slide + audio -> MP4 with Ken Burns zoom (no individual fades)."""
    n_frames = int(duration * FPS)
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,"
        f"zoompan=z='min(zoom+{ZOOM_SPEED},{ZOOM_MAX})':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={n_frames}:fps={FPS}:s=1920x1080"
    )
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(slide_path),
        "-i",          str(audio_path),
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
        "-vf", vf,
        "-t", str(duration),
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        str(out_path),
    ], check=True, capture_output=True)

def make_frame_clip(img, duration, out_path):
    """Single PIL frame -> silent MP4 clip of given duration."""
    png = TMP / f"_frame_{out_path.stem}.png"
    img.save(str(png))
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(png),
        "-c:v", "libx264", "-tune", "stillimage",
        "-t", str(duration),
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-an",
        str(out_path),
    ], check=True, capture_output=True)

def make_terminal_segment(frames_with_dur, audio_path, out_path, total_dur):
    """Animated terminal frames + audio -> MP4 segment."""
    frame_clips = []
    for i, (img, dur) in enumerate(frames_with_dur):
        clip = TMP / f"term_clip_{i:02d}.mp4"
        make_frame_clip(img, dur, clip)
        frame_clips.append(clip)

    concat_txt = TMP / "term_concat.txt"
    concat_txt.write_text("\n".join(f"file '{c.as_posix()}'" for c in frame_clips))

    silent = TMP / "term_silent.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(silent),
    ], check=True, capture_output=True)

    # merge silent video + TTS audio, trim to audio length
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(silent),
        "-i", str(audio_path),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-t", str(total_dur),
        str(out_path),
    ], check=True, capture_output=True)

def concat_xfade(segment_files, durations, out_path, fade=XFADE_DUR):
    """
    Concatenate segments with xfade video dissolve + acrossfade audio.
    Each offset = sum(durations[:i]) - i*fade  (correct xfade chaining formula).
    """
    n = len(segment_files)
    inputs = []
    for f in segment_files:
        inputs += ["-i", str(f)]

    if n == 1:
        subprocess.run(["ffmpeg", "-y", "-i", str(segment_files[0]), "-c", "copy", str(out_path)],
                       check=True, capture_output=True)
        return

    fv, fa = [], []
    prev_v, prev_a = "[0:v]", "[0:a]"

    for i in range(1, n):
        offset    = sum(durations[:i]) - i * fade
        out_v     = f"[v{i}]" if i < n - 1 else "[vout]"
        out_a     = f"[a{i}]" if i < n - 1 else "[aout]"
        fv.append(f"{prev_v}[{i}:v]xfade=transition=fade:duration={fade:.3f}:offset={offset:.3f}{out_v}")
        fa.append(f"{prev_a}[{i}:a]acrossfade=d={fade:.3f}:c1=tri:c2=tri{out_a}")
        prev_v, prev_a = out_v, out_a

    fc = ";".join(fv) + ";" + ";".join(fa)

    subprocess.run([
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", fc,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        str(out_path),
    ], check=True)

# ── Segments ──────────────────────────────────────────────────────────────────
SEGMENTS = [
    {
        "label": "hook",
        "type":  "slide",
        "slide": SLIDES / "pitch-slide-01.png",
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
        "label": "gap",
        "type":  "slide",
        "slide": SLIDES / "pitch-slide-02.png",
        "text": (
            "Solana Foundation's STRIDE monitors protocols with ten million or more in TVL. "
            "Maybe a hundred projects. "
            "There are thousands of DAOs, grant committees, and treasury multisigs below that line. "
            "They have nothing."
        ),
    },
    {
        "label": "solution",
        "type":  "slide",
        "slide": SLIDES / "pitch-slide-03.png",
        "text": (
            "Custos Nox is an open-source daemon. "
            "It watches Solana accounts over Helius WebSocket and fires an alert "
            "when a config change matches an attack pattern. "
            "Five detectors live today. "
            "Four map to the Drift attack chain: timelock removed, multisig weakened, "
            "nonce seeded, stale nonce executed. "
            "The fifth catches signer rotation. "
            "Any single alert would have stopped the drain."
        ),
    },
    {
        "label": "terminal",
        "type":  "terminal",
        "text": (
            "The tool is live right now. "
            "I'm running the devnet smoke harness — step one: remove the governance timelock. "
            "Transaction confirms in under two seconds. "
            "There — CRITICAL. "
            "Timelock dropped to zero, milliseconds after the transaction landed. "
            "The alert includes a Solscan link, the previous and current values, "
            "and a machine-readable reason code. "
            "This alone gives a DAO hours of warning."
        ),
    },
    {
        "label": "gtm",
        "type":  "slide",
        "slide": None,   # generated inline -> make_slide_05()
        "text": (
            "First users: Squads multisig operators — protocol treasuries, grant committees, "
            "hackathon prize pools. They're already on Discord. "
            "Integration is one webhook URL and a five-minute self-host. "
            "MIT licensed, no paid tiers. "
        ),
    },
    {
        "label": "vision",
        "type":  "slide",
        "slide": None,   # generated inline -> make_slide_06()
        "text": (
            "Long term: a hosted feed that any DAO subscribes to with zero infra. "
            "Top-50 Solana multisigs pre-watched. "
            "Any DAO. One click. Discord ping. Done."
        ),
    },
    {
        "label": "close",
        "type":  "slide",
        "slide": SLIDES / "pitch-slide-07.png",
        "text": (
            "I'm Yasya from Superteam Ukraine. "
            "Code is live on GitHub, demo runs on devnet, five detectors are watching right now. "
            "github dot com slash cryptoyasenka slash custos dash nox."
        ),
    },
]

# ── Main ──────────────────────────────────────────────────────────────────────
async def main():
    print("Generating improved slides ...")
    SEGMENTS[4]["slide"] = make_slide_05()
    SEGMENTS[5]["slide"] = make_slide_06()

    term_frames = build_term_frames()
    # duration of all fixed frames (all except last which is the hold)
    fixed_term_dur = sum(d for _, d in term_frames if d is not None)

    segment_files = []
    durations     = []

    for i, seg in enumerate(SEGMENTS):
        label = seg["label"]
        print(f"\n[{i+1}/{len(SEGMENTS)}] {label} ...")

        audio = TMP / f"audio_{i:02d}.mp3"
        video = TMP / f"seg_{i:02d}.mp4"

        await gen_audio(seg["text"], audio)
        dur = get_duration(audio)
        print(f"  audio: {dur:.1f}s")

        if seg["type"] == "slide":
            make_slide_segment(seg["slide"], audio, video, dur)

        elif seg["type"] == "terminal":
            hold = max(0.6, dur - fixed_term_dur)
            filled = [(img, d if d is not None else hold) for img, d in term_frames]
            print(f"  terminal anim: {fixed_term_dur:.1f}s fixed + {hold:.1f}s hold")
            make_terminal_segment(filled, audio, video, dur)

        segment_files.append(video)
        durations.append(dur)

    print(f"\nConcatenating {len(segment_files)} segments with xfade (fade={XFADE_DUR}s) ...")
    out = OUT_DIR / "f2-pitch-v2.mp4"
    concat_xfade(segment_files, durations, out, fade=XFADE_DUR)

    total = get_duration(out)
    size  = out.stat().st_size / 1024 / 1024
    print(f"\nDONE  ->  {out}")
    print(f"  Duration : {int(total//60)}:{int(total%60):02d}  ({total:.1f}s)")
    print(f"  Size     : {size:.1f} MB")

asyncio.run(main())
