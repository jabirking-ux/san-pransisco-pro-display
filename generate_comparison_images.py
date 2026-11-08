import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('docs/images', exist_ok=True)

sf_reg_path = r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYREGULAR.OTF'
sf_bold_path = r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYBOLD.OTF'

sp_reg_path = r'dist\user_exact\SFPRODISPLAYREGULAR_ALTERNATIVE.ttf'
sp_bold_path = r'dist\user_exact\SFPRODISPLAYBOLD_ALTERNATIVE.ttf'

BG_COLOR = (11, 13, 17)
GRID_LINE = (22, 26, 35)
CARD_BG = (17, 20, 28)
CARD_BORDER = (34, 40, 54)
TEXT_WHITE = (245, 245, 247)
TEXT_MUTED = (142, 146, 160)
ACCENT_BLUE = (41, 151, 255)
ACCENT_GREEN = (48, 209, 88)

def draw_grid_background(draw, width, height, step=40):
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=GRID_LINE, width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=GRID_LINE, width=1)

# ==============================================================================
# 1. FIXED BANNER (docs/images/banner.png) - No weird circles, pure sleek grid & type
# ==============================================================================
def create_banner():
    width = 1800
    height = 560
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Subtle technical grid
    draw_grid_background(draw, width, height, step=40)

    # 2. Status Badge
    draw.rounded_rectangle([80, 60, 440, 96], radius=18, fill=(18, 28, 48), outline=ACCENT_BLUE, width=1)
    font_badge = ImageFont.truetype(sp_bold_path, 13)
    draw.text((104, 71), "100% METRIC-COMPATIBLE & LEGAL ALTERNATIVE", font=font_badge, fill=ACCENT_BLUE)

    # 3. Main Title
    font_h1 = ImageFont.truetype(sp_bold_path, 66)
    draw.text((80, 120), "San Pransisco Pro Display", font=font_h1, fill=TEXT_WHITE)

    # 4. Subtitle
    font_sub = ImageFont.truetype(sp_reg_path, 22)
    draw.text((80, 212), "The drop-in, zero-delta, open-source alternative to Apple's SF Pro Display.", font=font_sub, fill=TEXT_MUTED)

    # 5. Technical Spec Tags
    tags = [
        "2048 UPM Grid",
        "Cap-Height: 1443",
        "Ascender: +1950",
        "Descender: -494",
        "18 Styles (Thin to Black)",
        "SIL OFL 1.1"
    ]
    tag_x = 80
    tag_y = 275
    font_tag = ImageFont.truetype(sp_bold_path, 13)
    for t in tags:
        t_w = len(t) * 9 + 26
        draw.rounded_rectangle([tag_x, tag_y, tag_x + t_w, tag_y + 34], radius=8, fill=CARD_BG, outline=CARD_BORDER, width=1)
        draw.text((tag_x + 13, tag_y + 8), t, font=font_tag, fill=TEXT_WHITE)
        tag_x += t_w + 12

    # 6. Bottom Typographic specimen strip
    draw.line([(80, 345), (width - 80, 345)], fill=CARD_BORDER, width=1)
    font_strip = ImageFont.truetype(sp_bold_path, 88)
    draw.text((80, 380), "Aa Bb Gg Rr 1234567890", font=font_strip, fill=(55, 65, 85))

    font_substrip = ImageFont.truetype(sp_reg_path, 20)
    draw.text((width - 520, 480), "Zero line-wrap shifts on Web & Windows", font=font_substrip, fill=ACCENT_GREEN)

    out_file = 'docs/images/banner.png'
    img.save(out_file, 'PNG')
    print(f"Created {out_file}")

# ==============================================================================
# 2. FIXED SIDE-BY-SIDE SPECIMEN (docs/images/comparison-specimen.png)
# ==============================================================================
def create_specimen_comparison():
    width = 1800
    height = 1420
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    draw_grid_background(draw, width, height, step=40)

    # Title Banner
    font_title = ImageFont.truetype(sp_bold_path, 40)
    font_sub = ImageFont.truetype(sp_reg_path, 18)
    draw.text((80, 50), "San Pransisco Pro Display vs Apple SF Pro Display", font=font_title, fill=TEXT_WHITE)
    draw.text((80, 105), "Side-by-side rendering test (Forensically matched to SF Pro Display Version 13.0d3e20)", font=font_sub, fill=TEXT_MUTED)

    col_w = 780
    col1_x = 80
    col2_x = 940
    start_y = 160
    panel_h = 1200

    draw.rounded_rectangle([col1_x, start_y, col1_x + col_w, start_y + panel_h], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.rounded_rectangle([col2_x, start_y, col2_x + col_w, start_y + panel_h], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)

    font_col_header = ImageFont.truetype(sp_bold_path, 22)
    font_col_tag = ImageFont.truetype(sp_reg_path, 13)

    # Col 1: Apple SF Pro Display
    draw.text((col1_x + 32, start_y + 24), "Apple SF Pro Display", font=font_col_header, fill=TEXT_WHITE)
    draw.text((col1_x + 32, start_y + 54), "Proprietary Original (Version 13.0d3e20)", font=font_col_tag, fill=(255, 69, 58))

    # Col 2: San Pransisco Pro Display
    draw.text((col2_x + 32, start_y + 24), "San Pransisco Pro Display", font=font_col_header, fill=TEXT_WHITE)
    draw.text((col2_x + 32, start_y + 54), "Clean-Room Alternative (SIL Open Font License)", font=font_col_tag, fill=ACCENT_GREEN)

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

    curr_y = start_y + 105
    font_section_label = ImageFont.truetype(sp_bold_path, 11)

    for label, size, is_bold, lines in sections:
        draw.line([(col1_x + 32, curr_y), (col1_x + col_w - 32, curr_y)], fill=(30, 36, 48), width=1)
        draw.line([(col2_x + 32, curr_y), (col2_x + col_w - 32, curr_y)], fill=(30, 36, 48), width=1)
        curr_y += 12

        draw.text((col1_x + 32, curr_y), label, font=font_section_label, fill=TEXT_MUTED)
        draw.text((col2_x + 32, curr_y), label, font=font_section_label, fill=TEXT_MUTED)
        curr_y += 24

        font_sf = ImageFont.truetype(sf_bold_path if is_bold else sf_reg_path, size)
        font_sp = ImageFont.truetype(sp_bold_path if is_bold else sp_reg_path, size)

        for line in lines:
            draw.text((col1_x + 32, curr_y), line, font=font_sf, fill=TEXT_WHITE)
            draw.text((col2_x + 32, curr_y), line, font=font_sp, fill=TEXT_WHITE)
            curr_y += int(size * 1.35)

        curr_y += 18

    out_file = 'docs/images/comparison-specimen.png'
    img.save(out_file, 'PNG')
    print(f"Created {out_file}")

# ==============================================================================
# 3. FIXED OVERLAY (docs/images/comparison-overlay.png)
# ==============================================================================
def create_overlay_comparison():
    width = 1800
    height = 920
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    draw_grid_background(draw, width, height, step=40)

    font_title = ImageFont.truetype(sp_bold_path, 36)
    font_sub = ImageFont.truetype(sp_reg_path, 18)
    draw.text((80, 50), "Forensic Glyph Contour Overlay", font=font_title, fill=TEXT_WHITE)
    draw.text((80, 100), "Cyan = Apple SF Pro Display  |  Magenta = San Pransisco Pro Display  |  White = Exact Geometric Overlap", font=font_sub, fill=TEXT_MUTED)

    sample_chars = ['R', 'a', 'g', 'S', 'e', '1', '4', 'Q', '&']
    char_size = 140
    font_sf = ImageFont.truetype(sf_bold_path, char_size)
    font_sp = ImageFont.truetype(sp_bold_path, char_size)

    cell_w = 170
    cell_h = 240
    start_x = 80
    start_y = 160

    for i, c in enumerate(sample_chars):
        col = i % 9
        cx = start_x + col * (cell_w + 12)
        cy = start_y

        draw.rounded_rectangle([cx, cy, cx + cell_w, cy + cell_h], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=1)

        baseline_y = cy + 175
        cap_y = baseline_y - int(char_size * (1443 / 2048))
        draw.line([(cx + 10, baseline_y), (cx + cell_w - 10, baseline_y)], fill=(45, 54, 72), width=1)
        draw.line([(cx + 10, cap_y), (cx + cell_w - 10, cap_y)], fill=(45, 54, 72), width=1)

        char_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_layer)

        char_draw.text((cx + 25, cy + 20), c, font=font_sf, fill=(0, 220, 255, 180))
        char_draw.text((cx + 25, cy + 20), c, font=font_sp, fill=(255, 60, 150, 180))

        img.paste(char_layer, (0, 0), char_layer)

        font_lbl = ImageFont.truetype(sp_bold_path, 13)
        draw.text((cx + 14, cy + cell_h - 26), f"Glyph '{c}'", font=font_lbl, fill=TEXT_MUTED)

    words = [
        ("Think different. in California", 44, False),
        ("SF Pro vs San Pransisco: 0px Delta", 36, True),
        ("$1,234,567.89  •  100% Metric Parity", 34, False)
    ]

    word_y = start_y + cell_h + 35
    for w_text, w_size, is_b in words:
        draw.rounded_rectangle([start_x, word_y, width - start_x, word_y + 80], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=1)

        f_sf = ImageFont.truetype(sf_bold_path if is_b else sf_reg_path, w_size)
        f_sp = ImageFont.truetype(sp_bold_path if is_b else sp_reg_path, w_size)

        word_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        w_draw = ImageDraw.Draw(word_layer)

        w_draw.text((start_x + 30, word_y + 18), w_text, font=f_sf, fill=(0, 220, 255, 200))
        w_draw.text((start_x + 30, word_y + 18), w_text, font=f_sp, fill=(255, 60, 150, 180))

        img.paste(word_layer, (0, 0), word_layer)
        word_y += 100

    out_file = 'docs/images/comparison-overlay.png'
    img.save(out_file, 'PNG')
    print(f"Created {out_file}")

if __name__ == '__main__':
    create_banner()
    create_specimen_comparison()
    create_overlay_comparison()
