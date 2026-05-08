"""
F2 pitch slides generator (Custos Nox).
Renders 7 PNG slides at 1920x1080 in brand dark theme.
Output: assets/pitch-slides/pitch-slide-NN.png
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pitch-slides"
OUT.mkdir(parents=True, exist_ok=True)
LOGO = Image.open(ROOT / "assets" / "logo.png").convert("RGBA")

W, H = 1920, 1080
BG = (10, 10, 10)
FG = (237, 237, 237)
MUTED = (113, 113, 122)
DIM = (82, 82, 91)
DIVIDER = (39, 39, 42)
GREEN = (74, 222, 128)
CYAN = (103, 232, 249)
RED = (239, 68, 68)
ORANGE = (251, 146, 60)


def font(name: str, size: int):
    return ImageFont.truetype(name, size)


# Font handles
F_BLACK = lambda s: font("seguibl.ttf", s)
F_BOLD = lambda s: font("segoeuib.ttf", s)
F_SEMI = lambda s: font("seguisb.ttf", s)
F_REG = lambda s: font("segoeui.ttf", s)
F_MONO = lambda s: font("consolab.ttf", s)


def new_slide():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    return img, d


def chrome(img, draw, slide_no: int, total: int = 7):
    """Brand chrome: top wordmark + bottom counter + dividers."""
    # Top: small logo + CUSTOS NOX wordmark
    logo_small = LOGO.resize((48, 48), Image.LANCZOS)
    img.paste(logo_small, (60, 50), logo_small)
    draw.text((120, 56), "CUSTOS NOX", font=F_BOLD(28), fill=FG)
    # Top right: subtitle
    sub = "F2 PITCH"
    sw = draw.textlength(sub, font=F_SEMI(20))
    draw.text((W - 60 - sw, 60), sub, font=F_SEMI(20), fill=MUTED)
    # Top divider
    draw.line([(60, 110), (W - 60, 110)], fill=DIVIDER, width=1)
    # Bottom divider
    draw.line([(60, H - 90), (W - 60, H - 90)], fill=DIVIDER, width=1)
    # Bottom: counter + project meta
    draw.text((60, H - 60), f"{slide_no:02d} / {total:02d}", font=F_SEMI(20), fill=MUTED)
    meta = "Frontier 2026  ·  Superteam Ukraine"
    mw = draw.textlength(meta, font=F_SEMI(20))
    draw.text((W - 60 - mw, H - 60), meta, font=F_SEMI(20), fill=MUTED)


def center_text(draw, text: str, fnt, y: int, fill=FG):
    tw = draw.textlength(text, font=fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)


def slide_1():
    """Hook: April 1, 2026 / $285M / 4 days / 0 alerts."""
    img, d = new_slide()
    chrome(img, d, 1)
    # Top eyebrow
    center_text(d, "DRIFT PROTOCOL", F_SEMI(36), 230, fill=MUTED)
    # Date
    center_text(d, "April 1, 2026", F_BLACK(108), 290, fill=FG)
    # Big number
    center_text(d, "$285M drained", F_BLACK(160), 430, fill=RED)
    # Breakdown line
    breakdown = "4 days   ·   3 governance changes   ·   0 alerts"
    center_text(d, breakdown, F_SEMI(56), 660, fill=FG)
    # Sub
    center_text(d, "Every step happened on chain. In public.", F_REG(40), 780, fill=MUTED)
    center_text(d, "Nobody noticed", F_BOLD(48), 850, fill=ORANGE)
    img.save(OUT / "pitch-slide-01.png")


def slide_2():
    """Problem: STRIDE protects ~100 protocols."""
    img, d = new_slide()
    chrome(img, d, 2)
    center_text(d, "THE GAP", F_SEMI(36), 220, fill=MUTED)
    # Headline
    center_text(d, "STRIDE protects", F_BLACK(96), 290, fill=FG)
    center_text(d, "~100 protocols", F_BLACK(140), 410, fill=CYAN)
    # Stat row
    y = 640
    # left stat
    d.text((W // 2 - 540, y), "$10M+ TVL", font=F_SEMI(40), fill=MUTED)
    d.text((W // 2 - 540, y + 56), "monitored", font=F_REG(36), fill=DIM)
    # right stat
    right_x = W // 2 + 60
    d.text((right_x, y), "Thousands of DAOs,", font=F_SEMI(40), fill=FG)
    d.text((right_x, y + 56), "treasuries, multisigs", font=F_REG(36), fill=FG)
    # Punchline
    center_text(d, "The other 99% have nothing", F_BOLD(60), 870, fill=ORANGE)
    img.save(OUT / "pitch-slide-02.png")


def slide_3():
    """Solution: 5 detectors live today."""
    img, d = new_slide()
    chrome(img, d, 3)
    center_text(d, "WHAT IT CATCHES", F_SEMI(36), 200, fill=MUTED)
    center_text(d, "5 detectors live today", F_BLACK(80), 260, fill=FG)
    # 5 detector cards in 2 rows (3 + 2)
    detectors = [
        ("TimelockRemoval", "CRITICAL", "Drift step: 6d → 0", RED),
        ("MultisigWeakening", "HIGH", "5-of-9 → 1-of-9", ORANGE),
        ("SignerSetChange", "HIGH", "Honest signers evicted", ORANGE),
        ("PrivilegedNonce", "CRITICAL", "Pre-signed drain seeded", RED),
        ("StaleNonceExecution", "HIGH", "Drain transaction lands", ORANGE),
    ]
    card_w, card_h = 540, 230
    gap = 30
    # Row 1: 3 cards
    row1_y = 430
    row1_total = card_w * 3 + gap * 2
    row1_x = (W - row1_total) // 2
    # Row 2: 2 cards
    row2_y = row1_y + card_h + gap
    row2_total = card_w * 2 + gap
    row2_x = (W - row2_total) // 2

    def card(x, y, name, sev, sev_color, hint):
        d.rectangle([(x, y), (x + card_w, y + card_h)], outline=DIVIDER, width=2)
        # severity pill
        pill_w = d.textlength(sev, font=F_BOLD(22)) + 32
        d.rectangle([(x + 24, y + 24), (x + 24 + pill_w, y + 24 + 36)], outline=sev_color, width=2)
        d.text((x + 24 + 16, y + 30), sev, font=F_BOLD(22), fill=sev_color)
        # name
        d.text((x + 24, y + 86), name, font=F_BOLD(36), fill=FG)
        # hint
        d.text((x + 24, y + 142), hint, font=F_REG(26), fill=MUTED)
        # bottom accent
        d.line([(x + 24, y + card_h - 24), (x + card_w - 24, y + card_h - 24)], fill=sev_color, width=1)

    for i in range(3):
        x = row1_x + i * (card_w + gap)
        n, s, h, c = detectors[i]
        card(x, row1_y, n, s, c, h)
    for i in range(2):
        x = row2_x + i * (card_w + gap)
        n, s, h, c = detectors[3 + i]
        card(x, row2_y, n, s, c, h)
    # Footer line
    center_text(d, "Sub-second alerts via Helius WebSocket", F_REG(32), 990, fill=GREEN)
    img.save(OUT / "pitch-slide-03.png")


def slide_4():
    """Traction: 205 tests / CI green / live dashboard."""
    img, d = new_slide()
    chrome(img, d, 4)
    center_text(d, "EVIDENCE", F_SEMI(36), 220, fill=MUTED)
    center_text(d, "Public repo  ·  Green CI", F_BLACK(96), 290, fill=FG)
    # Three stat cards in a row
    stats = [
        ("205", "tests passing", FG),
        ("5", "detectors live", GREEN),
        ("< 1s", "alert latency", CYAN),
    ]
    card_w, card_h = 440, 280
    gap = 60
    total = card_w * 3 + gap * 2
    start_x = (W - total) // 2
    y = 480

    for i, (num, label, color) in enumerate(stats):
        x = start_x + i * (card_w + gap)
        d.rectangle([(x, y), (x + card_w, y + card_h)], outline=DIVIDER, width=2)
        nw = d.textlength(num, font=F_BLACK(140))
        d.text((x + (card_w - nw) / 2, y + 60), num, font=F_BLACK(140), fill=color)
        lw = d.textlength(label, font=F_SEMI(32))
        d.text((x + (card_w - lw) / 2, y + 220), label, font=F_SEMI(32), fill=MUTED)
    # Live URL
    center_text(d, "custos-nox.up.railway.app", F_BOLD(48), 820, fill=GREEN)
    center_text(d, "Devnet smoke harness replays Drift steps in real time", F_REG(28), 900, fill=MUTED)
    img.save(OUT / "pitch-slide-04.png")


def slide_5():
    """GTM: First users + integration."""
    img, d = new_slide()
    chrome(img, d, 5)
    center_text(d, "WHO USES THIS", F_SEMI(36), 220, fill=MUTED)
    center_text(d, "First users:", F_BOLD(64), 290, fill=FG)
    center_text(d, "Squads multisig operators", F_BLACK(96), 380, fill=CYAN)
    center_text(d, "protocol treasuries  ·  grant committees  ·  hackathon prize pools", F_REG(36), 510, fill=MUTED)
    # 3 integration bullets
    bullets = [
        "1 webhook URL",
        "5-minute self-host",
        "Open issue tracker for detector requests",
    ]
    y = 660
    for line in bullets:
        center_text(d, line, F_SEMI(48), y, fill=FG)
        y += 80
    img.save(OUT / "pitch-slide-05.png")


def slide_6():
    """Vision (optional)."""
    img, d = new_slide()
    chrome(img, d, 6)
    center_text(d, "VISION", F_SEMI(36), 230, fill=MUTED)
    center_text(d, "Hosted feed", F_BLACK(108), 300, fill=FG)
    center_text(d, "Zero-infra monitoring", F_BLACK(108), 430, fill=CYAN)
    # Sub bullets
    y = 640
    items = [
        "Top-50 Solana multisigs by TVL — pre-watched",
        "Subscribe with one click. Discord ping. Slack ping. Done.",
        "Security layer between on-chain governance",
        "and the first Discord alert",
    ]
    for line in items:
        center_text(d, line, F_REG(36), y, fill=MUTED)
        y += 56
    img.save(OUT / "pitch-slide-06.png")


def slide_7():
    """Close: GitHub URL + name."""
    img, d = new_slide()
    chrome(img, d, 7)
    # Big logo center
    logo_big = LOGO.resize((180, 180), Image.LANCZOS)
    img.paste(logo_big, ((W - 180) // 2, 230), logo_big)
    # Wordmark
    center_text(d, "CUSTOS NOX", F_BLACK(96), 440, fill=FG)
    center_text(d, "Open-source attack monitor for Solana", F_REG(36), 560, fill=MUTED)
    # GitHub URL big
    center_text(d, "github.com/cryptoyasenka/custos-nox", F_BOLD(64), 680, fill=GREEN)
    # Author line
    center_text(d, "Yasya  ·  Superteam Ukraine  ·  Frontier 2026", F_SEMI(40), 830, fill=FG)
    img.save(OUT / "pitch-slide-07.png")


if __name__ == "__main__":
    slide_1()
    slide_2()
    slide_3()
    slide_4()
    slide_5()
    slide_6()
    slide_7()
    print(f"Done. Slides written to {OUT}")
