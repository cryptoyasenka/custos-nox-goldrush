"""
F3 Tech Demo Video generator
Terminal animation (PIL) + edge-tts voiceover -> MP4
Output: assets/f3-demo-final.mp4 (~2:35)
"""
import asyncio, subprocess, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "assets"
TMP = ROOT / "assets" / "_f3_tmp"
TMP.mkdir(exist_ok=True)

VOICE = "en-US-AriaNeural"
W, H = 1920, 1080

# Colors (GitHub dark theme)
BG      = "#0d1117"
FG      = "#c9d1d9"
GREEN   = "#3fb950"
RED     = "#ff6b6b"
ORANGE  = "#f0883e"
BLUE    = "#58a6ff"
GRAY    = "#8b949e"
YELLOW  = "#e3b341"
WHITE   = "#ffffff"

def get_font(size=22, bold=False):
    try:
        name = "consolab.ttf" if bold else "consola.ttf"
        return ImageFont.truetype(name, size)
    except Exception:
        try:
            return ImageFont.truetype("cour.ttf", size)
        except Exception:
            return ImageFont.load_default()

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def make_terminal_frame(left_lines, right_lines, title_left="Terminal 1 — attacker", title_right="Terminal 2 — custos daemon"):
    """Render split-screen terminal frame."""
    img = Image.new("RGB", (W, H), hex2rgb(BG))
    draw = ImageDraw.Draw(img)
    font = get_font(20)
    font_bold = get_font(20, bold=True)
    font_title = get_font(17)

    # Divider
    mid = W // 2
    draw.line([(mid, 0), (mid, H)], fill=hex2rgb(GRAY), width=1)

    # Titles
    draw.rectangle([0, 0, mid-1, 32], fill=hex2rgb("#161b22"))
    draw.rectangle([mid+1, 0, W, 32], fill=hex2rgb("#161b22"))
    draw.text((16, 8), title_left, font=font_title, fill=hex2rgb(GRAY))
    draw.text((mid+16, 8), title_right, font=font_title, fill=hex2rgb(GRAY))

    def render_lines(lines, x_start, y_start=44, max_width=mid-32):
        y = y_start
        line_h = 26
        for line in lines[-36:]:  # show last 36 lines
            if isinstance(line, str):
                text, color = line, FG
            else:
                text, color = line
            # Wrap long lines
            while len(text) > 80:
                draw.text((x_start, y), text[:80], font=font, fill=hex2rgb(color))
                y += line_h
                text = "  " + text[80:]
            draw.text((x_start, y), text, font=font, fill=hex2rgb(color))
            y += line_h

    render_lines(left_lines, 16)
    render_lines(right_lines, mid + 16)

    return img

# ── Terminal content ─────────────────────────────────────────────────────────

MULTISIG = "Chst4kw6...Pxg7z"
MULTISIG_FULL = "Chst4kw6UkFiDo6eEDUcrpXSoLg2p6BdZAYCcE5Pxg7z"
NONCE_FULL    = "EWu1Crhzs2Af6df3CbEyvALsqXvnbnDzQGvrSaEZUmGX"

DAEMON_STARTUP = [
    ("> npm run dev", BLUE),
    "",
    ("[custos] cluster=devnet", GRAY),
    ("[custos] rpc=https://api.devnet.solana.com", GRAY),
    ("[custos] detectors loaded: 5", GREEN),
    ("[custos] subscribe account=" + MULTISIG_FULL[:30] + "...", GRAY),
    ("[custos] subscribe account=" + NONCE_FULL[:30] + "...", GRAY),
    ("[custos] baseline seeded. watching.", GREEN),
    "",
]

ALERT_1 = [
    ("CRITICAL [squads-timelock-removal]", RED),
    ("  Timelock removed on multisig", FG),
    ("  " + MULTISIG_FULL, GRAY),
    ("  link: solscan.io/account/Chst4k...?cluster=devnet", BLUE),
    ('  ctx:  {"reason":"timelock_reduced",', GRAY),
    ('         "previousTimelockSeconds":86400,', GRAY),
    ('         "currentTimelockSeconds":0}', GRAY),
]

ALERT_2 = [
    ("HIGH [squads-multisig-weakening]", ORANGE),
    ("  Threshold weakened 3 -> 1 on multisig", FG),
    ("  " + MULTISIG_FULL, GRAY),
    ("  link: solscan.io/account/Chst4k...?cluster=devnet", BLUE),
    ('  ctx:  {"reason":"threshold_reduced",', GRAY),
    ('         "previousThreshold":3,', GRAY),
    ('         "currentThreshold":1}', GRAY),
]

ALERT_3 = [
    ("CRITICAL [privileged-nonce]", RED),
    ("  Nonce account initialized with attacker authority", FG),
    ("  " + NONCE_FULL, GRAY),
    ("  link: solscan.io/account/EWu1Cr...?cluster=devnet", BLUE),
    ('  ctx:  {"reason":"nonce_initialized",', GRAY),
    ('         "authority":"E9Q5UG..."}', GRAY),
]

TESTS_STALE = [
    ("> npm test src/detectors/stale-nonce-execution", BLUE),
    "",
    ("  StaleNonceExecutionDetector", WHITE),
    ("    fires HIGH when nonce advanced >1h after init", FG),
    ("    1) nonce advanced 65min after init -> HIGH  ✓", GREEN),
    ("    2) nonce advanced exactly 60min -> HIGH     ✓", GREEN),
    ("    3) nonce advanced 59min -> no alert         ✓", GREEN),
    ("    4) matches Drift execution pattern           ✓", GREEN),
    ("    5) authority mismatch -> no alert            ✓", GREEN),
    ("    ... 7 more cases",                               GRAY),
    "",
    ("  12 passing (284ms)", GREEN),
    "",
    ("  This is the detector that catches the drain itself.", FG),
    ("  Can't trigger live — needs 1h wait.", GRAY),
    ("  All 12 cases match the exact Drift pattern.", FG),
]

ARCH_LINES = [
    ("  ARCHITECTURE", YELLOW),
    "",
    ("  Helius WebSocket", BLUE),
    ("       |", GRAY),
    ("  AccountChangeEvent", FG),
    ("       |", GRAY),
    ("  +---------+  +---------+  +---------+  +---------+  +---------+", GRAY),
    ("  |Timelock |  |Multisig |  |Signer   |  |Nonce    |  |Stale    |", FG),
    ("  |Removal  |  |Weaken   |  |Set Chg  |  |Init     |  |Nonce    |", FG),
    ("  +---------+  +---------+  +---------+  +---------+  +---------+", GRAY),
    ("       |              |           |            |            |", GRAY),
    ("       +----[ FanOutAlertSink ]---+------------+------------+", GRAY),
    ("                    |", GRAY),
    ("          Discord  Slack  stdout", GREEN),
    "",
    ("  Per-detector 5s timeout. Hanging detector = low-sev alert.", GRAY),
    ("  205 tests. GitHub Actions CI on every push.", GREEN),
]

CLOSE_LINES = [
    "",
    ("  205 tests, all green.", GREEN),
    ("  GitHub Actions CI on every push.", GREEN),
    "",
    ("  Self-host:", FG),
    ("    git clone github.com/cryptoyasenka/custos-nox", BLUE),
    ("    cp .env.example .env", FG),
    ("    npm install && npm run dev", FG),
    "",
    ("  The code is at:", FG),
    ("  github.com/cryptoyasenka/custos-nox", WHITE),
    "",
]

# ── Segments: (left_lines, right_lines, voiceover, duration_hint_sec) ────────

def build_daemon(alerts):
    return DAEMON_STARTUP + alerts

SEGMENTS = [
    # 0:00-0:20 — intro, daemon running
    {
        "left":  ["C:\\Projects\\custos> "],
        "right": DAEMON_STARTUP,
        "text": (
            "This is Custos Nox, an open-source Solana security monitor. "
            "In Terminal 2, the daemon is running on devnet. "
            "It's subscribed via WebSocket to a Squads multisig and a durable-nonce account. "
            "Baseline state is seeded, so the first account change will be diffed correctly. "
            "I'm going to replay three setup steps from the Drift attack chain."
        ),
    },
    # 0:20-0:45 — timelock removal
    {
        "left":  [
            "C:\\Projects\\custos> ",
            (f"npm run smoke:timelock -- {MULTISIG_FULL[:20]}...", BLUE),
            "",
            ("  tx confirmed: 5Jwth...batD", GRAY),
        ],
        "right": build_daemon(ALERT_1 + [""]),
        "text": (
            "Step one: remove the governance timelock. "
            "The transaction confirms on devnet in about two seconds. "
            "There — CRITICAL. Timelock just dropped to zero. "
            "The alert includes a Solscan link, the previous and current values, "
            "and a machine-readable reason code. "
            "This alone gives the DAO hours of warning."
        ),
    },
    # 0:45-1:10 — multisig weakening
    {
        "left":  [
            "C:\\Projects\\custos> ",
            (f"npm run smoke:weaken -- {MULTISIG_FULL[:20]}...", BLUE),
            "",
            ("  tx confirmed: 5vAp7...Vrtm", GRAY),
        ],
        "right": build_daemon(ALERT_1 + [""] + ALERT_2 + [""]),
        "text": (
            "Step two: drop the signer threshold. "
            "HIGH severity. Threshold went from three-of-five to one-of-five — "
            "the multisig is now single-signer controlled. "
            "The attacker can now sign anything alone. "
            "Same pipeline: detector inspects the account diff, "
            "classifies severity, fans out to every configured sink simultaneously."
        ),
    },
    # 1:10-1:40 — nonce init
    {
        "left":  [
            "C:\\Projects\\custos> ",
            ("npm run smoke:nonce-init", BLUE),
            "",
            ("  tx confirmed: 56Hzo...hwPc", GRAY),
        ],
        "right": build_daemon(ALERT_1 + [""] + ALERT_2 + [""] + ALERT_3 + [""]),
        "text": (
            "Step three: seed a durable nonce under an attacker-controlled key. "
            "CRITICAL. Nonce initialized with authority controlled by the attacker. "
            "This is the mechanism that lets a pre-signed transaction land at any time "
            "in the future — on the attacker's schedule, not the DAO's. "
            "Three setup alerts, sub-second each. "
            "All the signals the DAO needed."
        ),
    },
    # 1:40-2:00 — stale nonce tests
    {
        "left":  TESTS_STALE,
        "right": build_daemon(ALERT_1 + [""] + ALERT_2 + [""] + ALERT_3 + [""]),
        "text": (
            "The fourth detector, StaleNonceExecutionDetector, watches that same nonce account. "
            "When a pre-signed transaction finally executes, it fires HIGH. "
            "I can't trigger this live without waiting an hour, "
            "but the unit suite covers the exact Drift drain pattern — "
            "twelve cases, all green. That's the final step. The drain itself."
        ),
    },
    # 2:00-2:20 — architecture
    {
        "left":  ARCH_LINES,
        "right": build_daemon(ALERT_1 + [""] + ALERT_2 + [""] + ALERT_3 + [""]),
        "text": (
            "The architecture is simple by design. "
            "Helius WebSocket delivers account changes. "
            "Five detectors inspect each event in parallel. "
            "The FanOut sink sends every alert to Discord, Slack, and stdout simultaneously. "
            "Per-detector five-second timeout — if a detector hangs, "
            "it surfaces as a low-severity operational alert instead of disappearing silently."
        ),
    },
    # 2:20-2:40 — close
    {
        "left":  CLOSE_LINES,
        "right": build_daemon(ALERT_1 + [""] + ALERT_2 + [""] + ALERT_3 + [""]),
        "text": (
            "205 tests, all green. GitHub Actions CI on every push. "
            "Self-host: clone the repo, set three environment variables, run npm dev. "
            "The code is at github dot com slash cryptoyasenka slash custos dash nox."
        ),
    },
]

async def gen_audio(text, path):
    import edge_tts
    comm = edge_tts.Communicate(text, VOICE, rate="+10%")
    await comm.save(str(path))

def get_duration(path):
    r = subprocess.run(["ffprobe","-v","quiet","-print_format","json","-show_streams",str(path)],
                       capture_output=True, text=True)
    return float(json.loads(r.stdout)["streams"][0]["duration"])

def make_video_segment(img_path, audio_path, out_path, duration):
    fade = 0.25
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(img_path),
        "-i", str(audio_path),
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "128k",
        "-vf", f"fade=t=in:st=0:d={fade},fade=t=out:st={duration-fade}:d={fade}",
        "-af", f"afade=t=in:st=0:d={fade},afade=t=out:st={duration-fade}:d={fade}",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(out_path)
    ], check=True, capture_output=True)

async def main():
    segment_files = []
    labels = ["intro","timelock","weaken","nonce-init","stale-test","arch","close"]

    for i, seg in enumerate(SEGMENTS):
        label = labels[i]
        print(f"[{i+1}/{len(SEGMENTS)}] {label} ...")

        img_path   = TMP / f"frame_{i:02d}.png"
        audio_path = TMP / f"audio_{i:02d}.mp3"
        video_path = TMP / f"seg_{i:02d}.mp4"

        # Render terminal frame
        frame = make_terminal_frame(seg["left"], seg["right"])
        frame.save(str(img_path))

        # Generate TTS
        await gen_audio(seg["text"], audio_path)
        duration = get_duration(audio_path)
        print(f"  duration: {duration:.1f}s")

        # Render video segment
        make_video_segment(img_path, audio_path, video_path, duration)
        segment_files.append(video_path)

    # Concatenate
    concat_list = TMP / "concat_f3.txt"
    with open(concat_list, "w") as f:
        for vf in segment_files:
            f.write(f"file '{vf.as_posix()}'\n")

    out_path = OUT_DIR / "f3-demo.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(out_path)
    ], check=True)

    duration = get_duration(out_path)
    print(f"\nDONE F3: {out_path}")
    print(f"  Duration: {int(duration//60)}:{int(duration%60):02d} ({duration:.1f}s)")
    print(f"  Size: {out_path.stat().st_size/1024/1024:.1f} MB")

asyncio.run(main())
