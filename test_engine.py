import os
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

def test_engine():
    user_path = r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYREGULAR.OTF'
    src_path = 'inter_extracted/extras/ttf/InterDisplay-Regular.ttf'
    out_path = 'test_engine_regular.ttf'
    
    user_font = TTFont(user_path)
    src_font = TTFont(src_path)
    
    user_cmap = user_font.getBestCmap()
    user_hmtx = user_font['hmtx']
    user_cff = user_font['CFF '].cff.topDictIndex[0].CharStrings
    
    src_cmap = src_font.getBestCmap()
    src_hmtx = src_font['hmtx']
    glyf = src_font['glyf']
    head = src_font['head']
    os2 = src_font['OS/2']
    hhea = src_font['hhea']
    user_os2 = user_font['OS/2']
    
    # Precompute bounds for user glyphs
    user_bounds = {}
    for cp, gname in user_cmap.items():
        if gname not in user_bounds:
            pen = BoundsPen(user_cff)
            user_cff[gname].draw(pen)
            if pen.bounds:
                user_bounds[gname] = pen.bounds
    
    # Stylistic glyph 'one' swap
    if 'one.ss01' in glyf and 'one' in glyf:
        one_g = glyf['one']
        one_ss = glyf['one.ss01']
        one_g.coordinates = one_ss.coordinates.copy()
        one_g.flags = one_ss.flags.copy()
        one_g.endPtsOfContours = one_ss.endPtsOfContours.copy()
        one_g.numberOfContours = one_ss.numberOfContours
        if hasattr(one_ss, 'program'):
            one_g.program = one_ss.program

    Sy_global = 1443.0 / 1490.0
    
    # Recalculate unscaled bounds for all source glyphs
    for name in glyf.keys():
        g = glyf[name]
        if hasattr(g, 'numberOfContours') and g.numberOfContours != 0:
            g.recalcBounds(glyf)
            
    transformed_glyphs = set()
    
    for cp, src_gname in src_cmap.items():
        if src_gname in transformed_glyphs:
            continue
            
        if cp in user_cmap:
            u_gname = user_cmap[cp]
            u_w, u_lsb = user_hmtx[u_gname]
            u_b = user_bounds.get(u_gname)
            
            if src_gname in glyf:
                g = glyf[src_gname]
                transformed_glyphs.add(src_gname)
                
                if g.numberOfContours > 0:
                    i_xMin, i_yMin, i_xMax, i_yMax = g.xMin, g.yMin, g.xMax, g.yMax
                    i_w = i_xMax - i_xMin
                    
                    if u_b and i_w > 0:
                        u_xMin, u_yMin, u_xMax, u_yMax = u_b
                        u_ink_w = u_xMax - u_xMin
                        
                        Sx = u_ink_w / i_w if i_w > 0 else 1.0
                        # Vertical scale
                        Sy = (u_yMax / i_yMax) if (i_yMax > 0 and abs(u_yMax - i_yMax*Sy_global) < 50) else Sy_global
                        
                        coords = g.coordinates
                        for i in range(len(coords)):
                            x, y = coords[i]
                            new_x = int(round(u_xMin + (x - i_xMin) * Sx))
                            new_y = int(round(y * Sy))
                            coords[i] = (new_x, new_y)
                            
                        g.xMin = u_xMin
                        g.xMax = u_xMin + int(round(u_ink_w))
                        g.yMin = int(round(i_yMin * Sy))
                        g.yMax = int(round(i_yMax * Sy))
                    else:
                        coords = g.coordinates
                        for i in range(len(coords)):
                            x, y = coords[i]
                            coords[i] = (x, int(round(y * Sy_global)))
                        g.recalcBounds(glyf)
                
                src_hmtx[src_gname] = (u_w, u_lsb)
    
    # Global metrics
    head.unitsPerEm = 2048
    os2.sTypoAscender = user_os2.sTypoAscender
    os2.sTypoDescender = user_os2.sTypoDescender
    os2.sTypoLineGap = user_os2.sTypoLineGap
    os2.usWinAscent = user_os2.usWinAscent
    os2.usWinDescent = user_os2.usWinDescent
    os2.sCapHeight = user_os2.sCapHeight
    os2.sxHeight = user_os2.sxHeight
    os2.usWeightClass = 400
    
    hhea.ascent = user_font['hhea'].ascent
    hhea.descent = user_font['hhea'].descent
    hhea.lineGap = user_font['hhea'].lineGap
    
    src_font.save(out_path)
    print("Test font saved successfully to", out_path)

test_engine()
