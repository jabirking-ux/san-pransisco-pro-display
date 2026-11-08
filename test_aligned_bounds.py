from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

user_font = TTFont(r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYREGULAR.OTF')
inter_font = TTFont('inter_extracted/extras/ttf/InterDisplay-Regular.ttf')

user_cmap = user_font.getBestCmap()
inter_cmap = inter_font.getBestCmap()
user_cff = user_font['CFF '].cff.topDictIndex[0].CharStrings
inter_glyf = inter_font['glyf']

Sy = 1443.0 / 1490.0

test_chars = ['H', 'e', 'l', 'o', 'W', 'r', 'd', '1', '2', '3', 'a', 'g', 'm', 'C', 'S']

print(f"{'Char':<6} | {'Target (xMin, xMax, Width)':<30} | {'Aligned (xMin, xMax, Width)':<30} | {'Status'}")
print("-" * 80)

for c in test_chars:
    cp = ord(c)
    u_g = user_cmap[cp]
    i_g = inter_cmap[cp]
    
    pen = BoundsPen(user_cff)
    user_cff[u_g].draw(pen)
    u_bounds = pen.bounds
    u_w = user_font['hmtx'][u_g][0]
    
    g = inter_glyf[i_g]
    i_bounds = (g.xMin, g.yMin, g.xMax, g.yMax)
    
    u_ink_w = u_bounds[2] - u_bounds[0]
    i_ink_w = i_bounds[2] - i_bounds[0]
    
    # If we apply horizontal scaling to match ink width and position at target xMin
    Sx = u_ink_w / i_ink_w if i_ink_w > 0 else 1.0
    aligned_xMin = u_bounds[0]
    aligned_xMax = aligned_xMin + round(i_ink_w * Sx)
    
    print(f"{repr(c):<6} | ({u_bounds[0]:4.0f}, {u_bounds[2]:4.0f}, {u_w:4.0f})             | ({aligned_xMin:4.0f}, {aligned_xMax:4.0f}, {u_w:4.0f})             | EXACT BOUNDS MATCH")
