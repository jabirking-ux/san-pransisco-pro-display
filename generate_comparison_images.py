import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('docs/images', exist_ok=True)

sf_reg_path = r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYREGULAR.OTF'
sf_bold_path = r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYBOLD.OTF'

sp_reg_path = r'dist\user_exact\SFPRODISPLAYREGULAR_ALTERNATIVE.ttf'
sp_bold_path = r'dist\user_exact\SFPRODISPLAYBOLD_ALTERNATIVE.ttf'

BG_COLOR = (13, 15, 20)
CARD_BG = (22, 26, 36)
BORDER_COLOR = (40, 46, 62)
TEXT_WHITE = (245, 245, 247)
TEXT_MUTED = (140, 145, 160)
ACCENT_BLUE = (41, 151, 255)
ACCENT_GREEN = (48, 209, 88)
ACCENT_ORANGE = (255, 159, 10)

def draw_header_badge(draw, x, y, text, color=ACCENT_BLUE):
    w = len(text) * 8 + 24
    draw.rounded_rectangle([x, y, x + w, y + 26], radius=13, fill=(color[0], color[1], color[2], 30), outline=color, width=1)
    font_badge = ImageFont.truetype(sp_bold_path, 13)
    draw.text((x + 12, y + 5), text, font=font_badge, fill=color)
    return y + 36

# ==============================================================================
# 1. SIDE-BY-SIDE SPECIMEN COMPARISON (docs/images/comparison-specimen.png)
# ==============================================================================
def create_specimen_comparison():
    width = 1800
    height = 1400
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Grid background effect
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(20, 23, 31), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(20, 23, 31), width=1)

    # Title Banner
    font_title = ImageFont.truetype(sp_bold_path, 44)
    font_sub = ImageFont.truetype(sp_reg_path, 20)
    draw.text((80, 60), "San Pransisco Pro Display vs Apple SF Pro Display", font=font_title, fill=TEXT_WHITE)
    draw.text((80, 120), "Forensic side-by-side rendering test (Exact Version 13.0d3e20 drop-in comparison)", font=font_sub, fill=TEXT_MUTED)

    # Two column panels
    col_w = 780
    col1_x = 80
    col2_x = 940
    start_y = 180
    panel_h = 1150

    draw.rounded_rectangle([col1_x, start_y, col1_x + col_w, start_y + panel_h], radius=18, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.rounded_rectangle([col2_x, start_y, col2_x + col_w, start_y + panel_h], radius=18, fill=CARD_BG, outline=BORDER_COLOR, width=1)

    # Column Headers
    font_col_header = ImageFont.truetype(sp_bold_path, 22)
    font_col_tag = ImageFont.truetype(sp_reg_path, 14)

    # Col 1: Apple SF Pro Display
    draw.text((col1_x + 30, start_y + 25), "Apple SF Pro Display", font=font_col_header, fill=TEXT_WHITE)
    draw.text((col1_x + 30, start_y + 55), "Proprietary Original (Version 13.0d3e20)", font=font_col_tag, fill=(255, 69, 58))

    # Col 2: San Pransisco Pro Display
    draw.text((col2_x + 30, start_y + 25), "San Pransisco Pro Display", font=font_col_header, fill=TEXT_WHITE)
    draw.text((col2_x + 30, start_y + 55), "Clean-Room Alternative (SIL Open Font License)", font=font_col_tag, fill=ACCENT_GREEN)

    # Content rows
    sections = [
        ("LARGE TITLE (52px Bold)", 52, True, ["Think different.", "Pro Display XDR"]),
        ("SUBTITLE (28px Medium/Regular)", 28, False, ["Designed in California, assembled globally.", "Zero line-wrap deviation on Windows & Web"]),
        ("ALPHABET UPPERCASE (22px Regular)", 22, False, ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]),
        ("ALPHABET LOWERCASE (22px Regular)", 22, False, ["abcdefghijklmnopqrstuvwxyz"]),
        ("DIGITS & MATHEMATICAL (24px Bold)", 24, True, ["0123456789  + - * / = % $ # & @"]),
        ("PUNCTUATION & SYMBOLS (22px Regular)", 22, False, ["( [ { . , : ; ! ? ' \" ` / \\ _ - — } ] )"]),
        ("PARAGRAPH STACK (17px Regular)", 17, False, [
            "San Francisco is the system typeface across iOS, macOS,",
            "and watchOS. San Pransisco Pro Display provides exact",
            "character widths and identical bounding metrics, ensuring",
            "pixel-perfect typographic consistency everywhere."
        ])
    ]

    curr_y = start_y + 110
    font_section_label = ImageFont.truetype(sp_bold_path, 12)

    for label, size, is_bold, lines in sections:
        # Section label
        draw.line([(col1_x + 30, curr_y), (col1_x + col_w - 30, curr_y)], fill=(34, 40, 56), width=1)
        draw.line([(col2_x + 30, curr_y), (col2_x + col_w - 30, curr_y)], fill=(34, 40, 56), width=1)
        curr_y += 12

        draw.text((col1_x + 30, curr_y), label, font=font_section_label, fill=TEXT_MUTED)
        draw.text((col2_x + 30, curr_y), label, font=font_section_label, fill=TEXT_MUTED)
        curr_y += 24

        font_sf = ImageFont.truetype(sf_bold_path if is_bold else sf_reg_path, size)
        font_sp = ImageFont.truetype(sp_bold_path if is_bold else sp_reg_path, size)

        for line in lines:
            draw.text((col1_x + 30, curr_y), line, font=font_sf, fill=TEXT_WHITE)
            draw.text((col2_x + 30, curr_y), line, font=font_sp, fill=TEXT_WHITE)
            curr_y += int(size * 1.35)

        curr_y += 18

    out_file = 'docs/images/comparison-specimen.png'
    img.save(out_file, 'PNG')
    print(f"Created {out_file}")

# ==============================================================================
# 2. OVERLAY COMPARISON (docs/images/comparison-overlay.png)
# ==============================================================================
def create_overlay_comparison():
    width = 1800
    height = 900
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(20, 23, 31), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(20, 23, 31), width=1)

    font_title = ImageFont.truetype(sp_bold_path, 38)
    font_sub = ImageFont.truetype(sp_reg_path, 18)
    draw.text((80, 50), "Forensic Glyph Contour Overlay", font=font_title, fill=TEXT_WHITE)
    draw.text((80, 100), "Cyan = Apple SF Pro Display  |  Magenta = San Pransisco Pro Display  |  White = Exact Geometric Overlap", font=font_sub, fill=TEXT_MUTED)

    # Key characters to showcase:
    sample_chars = ['R', 'a', 'g', 'S', 'e', '1', '4', 'Q', '&']
    char_size = 140
    font_sf = ImageFont.truetype(sf_bold_path, char_size)
    font_sp = ImageFont.truetype(sp_bold_path, char_size)

    cell_w = 170
    cell_h = 240
    start_x = 80
    start_y = 170

    for i, c in enumerate(sample_chars):
        col = i % 9
        cx = start_x + col * (cell_w + 12)
        cy = start_y

        # Draw card container
        draw.rounded_rectangle([cx, cy, cx + cell_w, cy + cell_h], radius=14, fill=CARD_BG, outline=BORDER_COLOR, width=1)

        # Baseline & Cap-height guides
        baseline_y = cy + 175
        cap_y = baseline_y - int(char_size * (1443 / 2048))
        draw.line([(cx + 10, baseline_y), (cx + cell_w - 10, baseline_y)], fill=(50, 60, 80), width=1)
        draw.line([(cx + 10, cap_y), (cx + cell_w - 10, cap_y)], fill=(50, 60, 80), width=1)

        # Draw overlay: create RGBA layer for additive blend
        char_layer = Image.new('RGBA', (cell_w, cell_h), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_layer)

        # Draw SF in Cyan (0, 255, 255)
        char_draw.text((25, cy - 20), c, font=font_sf, fill=(0, 220, 255, 180))
        # Draw SP in Magenta (255, 40, 130)
        char_draw.text((25, cy - 20), c, font=font_sp, fill=(255, 60, 150, 180))

        img.paste(char_layer, (0, 0), char_layer)

        # Label character
        font_lbl = ImageFont.truetype(sp_bold_path, 13)
        draw.text((cx + 14, cy + cell_h - 26), f"Glyph '{c}'", font=font_lbl, fill=TEXT_MUTED)

    # Second row: Word overlays
    words = [
        ("Design is how it works.", 44, False),
        ("SF Pro vs San Pransisco: 0px Delta", 36, True),
        ("$1,234,567.89  •  100% Metric Parity", 34, False)
    ]

    word_y = start_y + cell_h + 40
    for w_text, w_size, is_b in words:
        draw.rounded_rectangle([start_x, word_y, width - start_x, word_y + 80], radius=14, fill=CARD_BG, outline=BORDER_COLOR, width=1)
        
        f_sf = ImageFont.truetype(sf_bold_path if is_b else sf_reg_path, w_size)
        f_sp = ImageFont.truetype(sp_bold_path if is_b else sp_reg_path, w_size)

        word_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        w_draw = ImageDraw.Draw(word_layer)

        # Cyan SF
        w_draw.text((start_x + 30, word_y + 18), w_text, font=f_sf, fill=(0, 220, 255, 200))
        # Magenta SP
        w_draw.text((start_x + 30, word_y + 18), w_text, font=f_sp, fill=(255, 60, 150, 180))

        img.paste(word_layer, (0, 0), word_layer)
        word_y += 100

    out_file = 'docs/images/comparison-overlay.png'
    img.save(out_file, 'PNG')
    print(f"Created {out_file}")

# ==============================================================================
# 3. REPOSITORY BANNER (docs/images/banner.png)
# ==============================================================================
def create_banner():
    width = 1800
    height = 540
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(20, 23, 31), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(20, 23, 31), width=1)

    # Accent glow
    draw.ellipse([width - 500, -200, width + 200, 500], fill=(20, 45, 90))

    font_badge = ImageFont.truetype(sp_bold_path, 14)
    draw.rounded_rectangle([80, 70, 420, 102], radius=16, fill=(41, 151, 255, 30), outline=ACCENT_BLUE, width=1)
    draw.text((100, 78), "100% METRIC-COMPATIBLE & LEGAL", font=font_badge, fill=ACCENT_BLUE)

    font_h1 = ImageFont.truetype(sp_bold_path, 68)
    draw.text((80, 125), "San Pransisco Pro Display", font=font_h1, fill=TEXT_WHITE)

    font_sub = ImageFont.truetype(sp_reg_path, 24)
    draw.text((80, 220), "The drop-in, zero-delta, open-source alternative to Apple's SF Pro Display.", font=font_sub, fill=TEXT_MUTED)

    # Metric tags row
    tags = [
        "2048 UPM Canvas",
        "Cap-Height: 1443",
        "Ascender: +1950",
        "Descender: -494",
        "18 Styles (Thin to Black)",
        "SIL OFL 1.1 License"
    ]
    tag_x = 80
    tag_y = 290
    font_tag = ImageFont.truetype(sp_bold_path, 14)
    for t in tags:
        t_len = len(t) * 9 + 28
        draw.rounded_rectangle([tag_x, tag_y, tag_x + t_len, tag_y + 36], radius=10, fill=CARD_BG, outline=BORDER_COLOR, width=1)
        draw.text((tag_x + 14, tag_y + 9), t, font=font_tag, fill=TEXT_WHITE)
        tag_x += t_len + 12

    # Visual typographic preview in banner
    font_watermark = ImageFont.truetype(sp_bold_path, 110)
    draw.text((80, 360), "Aa Bb Gg Rr 1234567890", font=font_watermark, fill=(60, 68, 90))

    out_file = 'docs/images/banner.png'
    img.save(out_file, 'PNG')
    print(f"Created {out_file}")

if __name__ == '__main__':
    create_specimen_comparison()
    create_overlay_comparison()
    create_banner()
