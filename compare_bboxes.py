from fontTools.ttLib import TTFont

user_font = TTFont(r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYREGULAR.OTF')
inter_font = TTFont('inter_extracted/extras/ttf/InterDisplay-Regular.ttf')

user_cmap = user_font.getBestCmap()
inter_cmap = inter_font.getBestCmap()
user_cff = user_font['CFF '].cff.topDictIndex[0].CharStrings
inter_glyf = inter_font['glyf']

from fontTools.pens.boundsPen import BoundsPen

test_chars = ['H', 'O', 'x', 'n', '1', 'g', 'a', 't', 'p', 'l', '.', ',']

print(f"{'Char':<6} | {'User SF BBox (xMin, yMin, xMax, yMax)':<35} | {'Inter BBox (xMin, yMin, xMax, yMax)':<35}")
print("-" * 80)

for c in test_chars:
    cp = ord(c)
    u_g = user_cmap[cp]
    i_g = inter_cmap[cp]
    
    pen = BoundsPen(user_cff)
    user_cff[u_g].draw(pen)
    u_bounds = pen.bounds
    
    i_bounds = (inter_glyf[i_g].xMin, inter_glyf[i_g].yMin, inter_glyf[i_g].xMax, inter_glyf[i_g].yMax)
    
    print(f"{repr(c):<6} | {str(u_bounds):<35} | {str(i_bounds):<35}")
