from fontTools.ttLib import TTFont

ref = TTFont('references/SF-Pro-Display-Regular.otf')
gen = TTFont('dist/ttf/SanPransiscoProDisplay-Regular.ttf')

ref_cmap = ref.getBestCmap()
gen_cmap = gen.getBestCmap()

ref_hmtx = ref['hmtx']
gen_hmtx = gen['hmtx']

print("=== VERTICAL METRICS ===")
for t in ['OS/2', 'hhea']:
    for attr in ['sTypoAscender', 'sTypoDescender', 'sTypoLineGap', 'usWinAscent', 'usWinDescent', 'sxHeight', 'sCapHeight', 'ascent', 'descent', 'lineGap']:
        if hasattr(ref[t], attr) or hasattr(gen[t], attr):
            v_ref = getattr(ref[t], attr, 'N/A')
            v_gen = getattr(gen[t], attr, 'N/A')
            match = "EXACT MATCH" if v_ref == v_gen else "MISMATCH"
            print(f"{t}.{attr:16s}: Ref={str(v_ref):<6} Gen={str(v_gen):<6} [{match}]")

print("\n=== SAMPLE ADVANCE WIDTHS (ASCII) ===")
all_match = True
mismatches = []
for cp in range(32, 127):
    ch = chr(cp)
    if cp in ref_cmap and cp in gen_cmap:
        w_ref = ref_hmtx[ref_cmap[cp]][0]
        w_gen = gen_hmtx[gen_cmap[cp]][0]
        if w_ref != w_gen:
            all_match = False
            mismatches.append((ch, w_ref, w_gen))

if all_match:
    print("ALL ASCII glyph advance widths MATCH 100% EXACTLY (0 unit difference)!")
else:
    print(f"Mismatches found ({len(mismatches)}):", mismatches)

# Print a nice table of representative words and letters
sample_text = "The quick brown fox jumps over the lazy dog 1234567890"
ref_total_width = sum(ref_hmtx[ref_cmap[ord(c)]][0] for c in sample_text)
gen_total_width = sum(gen_hmtx[gen_cmap[ord(c)]][0] for c in sample_text)

print(f"\nTotal width of pangram sentence:")
print(f"Text: '{sample_text}'")
print(f"SF Pro Display:          {ref_total_width} font units")
print(f"San Pransisco Pro:       {gen_total_width} font units")
print(f"Delta:                   {gen_total_width - ref_total_width} units ({((gen_total_width - ref_total_width)/ref_total_width)*100:.4f}%)")
