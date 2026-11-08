import os
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph

def transform_font(source_path, ref_path, output_path, family_name, subfamily_name, weight_class):
    font = TTFont(source_path)
    ref = TTFont(ref_path)

    ref_cmap = ref.getBestCmap()
    ref_hmtx = ref['hmtx']
    src_cmap = font.getBestCmap()
    src_hmtx = font['hmtx']
    glyf = font['glyf']
    head = font['head']
    os2 = font['OS/2']
    hhea = font['hhea']
    ref_os2 = ref['OS/2']

    # 1. Metric calibration
    head.unitsPerEm = 2048
    os2.sTypoAscender = 1950
    os2.sTypoDescender = -494
    os2.sTypoLineGap = 0
    os2.usWinAscent = 1950
    os2.usWinDescent = 494
    os2.sCapHeight = 1443
    os2.sxHeight = getattr(ref_os2, 'sxHeight', 1040)
    os2.usWeightClass = weight_class

    hhea.ascent = 1950
    hhea.descent = -494
    hhea.lineGap = 0

    # 2. Check glyph substitutions for closer match (e.g. digit 1 with serif)
    # If one.ss01 exists, we can use its shape for 'one'
    if 'one.ss01' in glyf and 'one' in glyf:
        print("  Applying flagged serif 'one' alternate...")
        # copy coordinates from one.ss01 to one
        one_g = glyf['one']
        one_ss = glyf['one.ss01']
        one_g.coordinates = one_ss.coordinates.copy()
        one_g.flags = one_ss.flags.copy()
        one_g.endPtsOfContours = one_ss.endPtsOfContours.copy()
        one_g.numberOfContours = one_ss.numberOfContours
        if hasattr(one_ss, 'program'):
            one_g.program = one_ss.program

    # 3. Horizontal metric calibration & glyph recentering
    adjusted_count = 0
    shifted_glyphs = set()

    for cp, src_gname in src_cmap.items():
        if cp in ref_cmap:
            ref_gname = ref_cmap[cp]
            target_w, ref_lsb = ref_hmtx[ref_gname]
            cur_w, cur_lsb = src_hmtx[src_gname]

            diff_w = target_w - cur_w
            if diff_w != 0:
                adjusted_count += 1
                dx = int(round(diff_w / 2.0))

                # Update glyph coordinates if not already shifted
                if src_gname not in shifted_glyphs and src_gname in glyf:
                    shifted_glyphs.add(src_gname)
                    g = glyf[src_gname]
                    if g.numberOfContours > 0:
                        # Simple glyph
                        coords = g.coordinates
                        for i in range(len(coords)):
                            coords[i] = (coords[i][0] + dx, coords[i][1])
                        g.xMin += dx
                        g.xMax += dx
                    elif g.numberOfContours < 0:
                        # Composite glyph
                        if hasattr(g, 'components'):
                            for comp in g.components:
                                comp.x += dx
                        g.recalcBounds(glyf)

                new_lsb = cur_lsb + dx
                src_hmtx[src_gname] = (target_w, new_lsb)

    # 4. Recalculate font bounding box
    for name in glyf.keys():
        g = glyf[name]
        if hasattr(g, 'numberOfContours') and g.numberOfContours != 0:
            g.recalcBounds(glyf)

    x_mins = [glyf[g].xMin for g in glyf.keys() if hasattr(glyf[g], 'xMin')]
    x_maxs = [glyf[g].xMax for g in glyf.keys() if hasattr(glyf[g], 'xMax')]
    y_mins = [glyf[g].yMin for g in glyf.keys() if hasattr(glyf[g], 'yMin')]
    y_maxs = [glyf[g].yMax for g in glyf.keys() if hasattr(glyf[g], 'yMax')]
    if x_mins and x_maxs and y_mins and y_maxs:
        head.xMin = min(x_mins)
        head.xMax = max(x_maxs)
        head.yMin = min(y_mins)
        head.yMax = max(y_maxs)
        hhea.minLeftSideBearing = min(src_hmtx.metrics[g][1] for g in src_hmtx.metrics.keys())
        hhea.xMaxExtent = max(src_hmtx.metrics[g][1] + (glyf[g].xMax - glyf[g].xMin if hasattr(glyf[g], 'xMax') else 0) for g in src_hmtx.metrics.keys())

    # 5. Metadata / Name table updates
    ps_name = f"{family_name.replace(' ', '')}-{subfamily_name.replace(' ', '')}"
    full_name = f"{family_name} {subfamily_name}"
    unique_id = f"1.000;AGY;{ps_name}"

    name_table = font['name']
    name_records = {
        1: family_name,
        2: subfamily_name,
        3: unique_id,
        4: full_name,
        5: "Version 1.000",
        6: ps_name,
        7: "San Pransisco is a clean-room engineered, metric-compatible alternative typeface.",
        8: "Antigravity Typographic Laboratories",
        9: "Rasmus Andersson & Antigravity Contributors",
        11: "https://github.com/google/antigravity",
        13: "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
        14: "http://scripts.sil.org/OFL",
        16: family_name,
        17: subfamily_name,
    }

    # Clear old names and re-populate
    new_names = []
    # Add platform 3 (Windows Unicode BMP) and platform 1 (Macintosh Roman)
    for name_id, text in name_records.items():
        # Windows English
        name_table.setName(text, name_id, platformID=3, platEncID=1, langID=0x0409)
        # Mac English
        name_table.setName(text, name_id, platformID=1, platEncID=0, langID=0)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    font.save(output_path)
    print(f"Successfully generated {output_path} (adjusted {adjusted_count} glyph widths)")

if __name__ == '__main__':
    src = 'inter_extracted/extras/ttf/InterDisplay-Regular.ttf'
    ref = 'references/SF-Pro-Display-Regular.otf'
    out = 'dist/ttf/SanPransiscoProDisplay-Regular.ttf'
    transform_font(src, ref, out, 'San Pransisco Pro Display', 'Regular', 400)
