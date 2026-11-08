import math
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

user_font = TTFont(r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYREGULAR.OTF')
inter_font = TTFont('inter_extracted/extras/ttf/InterDisplay-Regular.ttf')

user_cmap = user_font.getBestCmap()
inter_cmap = inter_font.getBestCmap()
user_cff = user_font['CFF '].cff.topDictIndex[0].CharStrings
inter_glyf = inter_font['glyf']

Sy = 1443.0 / 1490.0

test_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

results = []
for c in test_chars:
    cp = ord(c)
    if cp in user_cmap and cp in inter_cmap:
        u_g = user_cmap[cp]
        i_g = inter_cmap[cp]
        
        pen = BoundsPen(user_cff)
        user_cff[u_g].draw(pen)
        u_bounds = pen.bounds
        
        g = inter_glyf[i_g]
        i_bounds = (g.xMin, g.yMin, g.xMax, g.yMax)
        
        # Test scaled bounds
        scaled_yMax = round(i_bounds[3] * Sy)
        scaled_yMin = round(i_bounds[1] * Sy)
        
        u_h = u_bounds[3] - u_bounds[1]
        s_h = scaled_yMax - scaled_yMin
        
        results.append((c, u_bounds[3], scaled_yMax, abs(u_bounds[3] - scaled_yMax), u_h, s_h))

print(f"{'Char':<6} | {'Target yMax':<12} | {'Scaled yMax':<12} | {'Diff':<6} | {'Target H':<10} | {'Scaled H':<10}")
print("-" * 65)
for r in results[:20]:
    print(f"{repr(r[0]):<6} | {r[1]:<12} | {r[2]:<12} | {r[3]:<6} | {r[4]:<10} | {r[5]:<10}")

max_diff = max(r[3] for r in results)
avg_diff = sum(r[3] for r in results) / len(results)
print(f"\nAcross all 62 alphanumeric characters:")
print(f"  Max yMax difference after Sy scaling: {max_diff} units (out of 2048 UPM, {max_diff/2048*100:.2f}%)")
print(f"  Average yMax difference: {avg_diff:.2f} units ({avg_diff/2048*100:.2f}%)")
