import os
from fontTools.ttLib import TTFont

dir_path = r'C:\Users\User\Downloads\Compressed\sf-pro-display'

fonts_info = {}
for f in os.listdir(dir_path):
    if f.lower().endswith('.otf'):
        path = os.path.join(dir_path, f)
        font = TTFont(path)
        name = font['name']
        ps_name = name.getDebugName(6)
        subfamily = name.getDebugName(2)
        os2 = font['OS/2']
        hhea = font['hhea']
        cmap = font.getBestCmap()
        hmtx = font['hmtx']
        
        fonts_info[f] = {
            'file': f,
            'ps_name': ps_name,
            'subfamily': subfamily,
            'weight': os2.usWeightClass,
            'capHeight': os2.sCapHeight,
            'xHeight': os2.sxHeight,
            'typoAscender': os2.sTypoAscender,
            'typoDescender': os2.sTypoDescender,
            'winAscent': os2.usWinAscent,
            'winDescent': os2.usWinDescent,
            'hheaAscent': hhea.ascent,
            'hheaDescent': hhea.descent,
            'cmap_count': len(cmap),
            'glyph_count': len(font.getGlyphOrder()),
            'gpos_features': [r.FeatureTag for r in font['GPOS'].table.FeatureList.FeatureRecord] if 'GPOS' in font else [],
            'gsub_features': [r.FeatureTag for r in font['GSUB'].table.FeatureList.FeatureRecord] if 'GSUB' in font else [],
        }

for f, info in sorted(fonts_info.items()):
    print(f"{info['file']:32s} | PS: {info['ps_name']:28s} | W: {info['weight']:3d} | CapH: {info['capHeight']} | xH: {info['xHeight']} | Glyphs: {info['glyph_count']:4d} | Cmap: {info['cmap_count']:4d} | GPOS: {info['gpos_features']}")
