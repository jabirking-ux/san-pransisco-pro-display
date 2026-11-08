import os
from fontTools.ttLib import TTFont

dir_path = r'C:\Users\User\Downloads\Compressed\sf-pro-display'

for f in os.listdir(dir_path):
    if f.lower().endswith(('.otf', '.ttf')):
        full_path = os.path.join(dir_path, f)
        font = TTFont(full_path)
        head = font['head']
        os2 = font['OS/2']
        hhea = font['hhea']
        name = font['name']
        cmap = font.getBestCmap()
        
        family = name.getDebugName(1)
        subfamily = name.getDebugName(2)
        full_n = name.getDebugName(4)
        ps_name = name.getDebugName(6)
        version = name.getDebugName(5)
        
        print(f"File: {f}")
        print(f"  Names: Family='{family}', Subfamily='{subfamily}', Full='{full_n}', PS='{ps_name}', Ver='{version}'")
        print(f"  Metrics: UPM={head.unitsPerEm}, Weight={os2.usWeightClass}, CapH={os2.sCapHeight}, xH={os2.sxHeight}")
        print(f"  Vertical: TypoAsc={os2.sTypoAscender}, TypoDesc={os2.sTypoDescender}, WinAsc={os2.usWinAscent}, WinDesc={os2.usWinDescent}, hheaAsc={hhea.ascent}, hheaDesc={hhea.descent}")
        print(f"  Glyphs: total_glyphs={len(font.getGlyphOrder())}, cmap_codepoints={len(cmap)}")
        print(f"  Tables: {list(font.keys())}")
        print("-" * 70)
