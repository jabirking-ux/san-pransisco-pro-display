import os
from fontTools.ttLib import TTFont

user_ref_path = r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYREGULAR.OTF'
user_font = TTFont(user_ref_path)

print("User Font Tables:", list(user_font.keys()))
print("User Font CFF fontNames:", user_font['CFF '].cff.fontNames)
user_cmap = user_font.getBestCmap()
user_hmtx = user_font['hmtx']

print(f"Total mapped characters in user's SFPRODISPLAYREGULAR: {len(user_cmap)}")

# Check ASCII
ascii_chars = [chr(i) for i in range(32, 127)]
print("\nSample Widths from User's Font:")
for c in "Hello World! 1234567890":
    cp = ord(c)
    if cp in user_cmap:
        gname = user_cmap[cp]
        print(f"  '{c}': width={user_hmtx[gname][0]}, lsb={user_hmtx[gname][1]}")

# Compare with our generated SanPransiscoProDisplay-Regular.ttf
gen_path = 'dist/ttf/SanPransiscoProDisplay-Regular.ttf'
if os.path.exists(gen_path):
    gen_font = TTFont(gen_path)
    gen_cmap = gen_font.getBestCmap()
    gen_hmtx = gen_font['hmtx']
    
    matches = 0
    total = 0
    diffs = []
    for cp, gname in user_cmap.items():
        if cp in gen_cmap:
            total += 1
            w_u = user_hmtx[gname][0]
            w_g = gen_hmtx[gen_cmap[cp]][0]
            if w_u == w_g:
                matches += 1
            else:
                diffs.append((chr(cp) if 32 <= cp <= 126 else f"U+{cp:04X}", w_u, w_g))
    print(f"\nComparison with generated font:")
    print(f"  Common codepoints: {total}")
    print(f"  Exact width matches: {matches} / {total} ({matches/total*100:.2f}%)")
    if diffs:
        print(f"  First 10 mismatches: {diffs[:10]}")
