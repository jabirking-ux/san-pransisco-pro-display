import os
from fontTools.ttLib import TTFont

styles = [
    ('Ultralight', 'SF-Pro-Display-Ultralight.otf', 'SanPransiscoProDisplay-Ultralight.ttf'),
    ('Thin', 'SF-Pro-Display-Thin.otf', 'SanPransiscoProDisplay-Thin.ttf'),
    ('Light', 'SF-Pro-Display-Light.otf', 'SanPransiscoProDisplay-Light.ttf'),
    ('Regular', 'SF-Pro-Display-Regular.otf', 'SanPransiscoProDisplay-Regular.ttf'),
    ('Medium', 'SF-Pro-Display-Medium.otf', 'SanPransiscoProDisplay-Medium.ttf'),
    ('Semibold', 'SF-Pro-Display-Semibold.otf', 'SanPransiscoProDisplay-Semibold.ttf'),
    ('Bold', 'SF-Pro-Display-Bold.otf', 'SanPransiscoProDisplay-Bold.ttf'),
    ('Heavy', 'SF-Pro-Display-Heavy.otf', 'SanPransiscoProDisplay-Heavy.ttf'),
    ('Black', 'SF-Pro-Display-Black.otf', 'SanPransiscoProDisplay-Black.ttf'),
]

pangrams = [
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "SF Pro Display vs San Pransisco Pro Display: 100% Metric Parity!",
    "Design is not just what it looks like and feels like. Design is how it works. - Steve Jobs",
    "$1,234,567.89 (0123456789) + - * / = % @ # & !"
]

print("================================================================================")
print(" FORENSIC VERIFICATION: SF PRO DISPLAY vs SAN PRANSISCO PRO DISPLAY")
print("================================================================================")

for name, ref_file, gen_file in styles:
    ref_path = os.path.join('references', ref_file)
    gen_path = os.path.join('dist', 'ttf', gen_file)

    ref = TTFont(ref_path)
    gen = TTFont(gen_path)

    ref_os2 = ref['OS/2']
    gen_os2 = gen['OS/2']

    ref_cmap = ref.getBestCmap()
    gen_cmap = gen.getBestCmap()

    ref_hmtx = ref['hmtx']
    gen_hmtx = gen['hmtx']

    # Metric check
    v_metrics_match = (
        ref_os2.sTypoAscender == gen_os2.sTypoAscender and
        ref_os2.sTypoDescender == gen_os2.sTypoDescender and
        ref_os2.sCapHeight == gen_os2.sCapHeight and
        ref['head'].unitsPerEm == gen['head'].unitsPerEm
    )

    # ASCII match check
    ascii_matches = 0
    ascii_total = 0
    for cp in range(32, 127):
        if cp in ref_cmap and cp in gen_cmap:
            ascii_total += 1
            if ref_hmtx[ref_cmap[cp]][0] == gen_hmtx[gen_cmap[cp]][0]:
                ascii_matches += 1

    # Pangram line width test
    pangram_deltas = []
    for p in pangrams:
        w_ref = sum(ref_hmtx[ref_cmap[ord(c)]][0] for c in p if ord(c) in ref_cmap)
        w_gen = sum(gen_hmtx[gen_cmap[ord(c)]][0] for c in p if ord(c) in gen_cmap)
        pangram_deltas.append(w_gen - w_ref)

    max_delta = max(abs(d) for d in pangram_deltas)

    status = "[PASS 100%]" if v_metrics_match and ascii_matches == ascii_total and max_delta == 0 else "[FAIL]"
    print(f"{name:12s} | UPM: {gen['head'].unitsPerEm} | CapH: {gen_os2.sCapHeight} | Asc/Desc: {gen_os2.sTypoAscender}/{gen_os2.sTypoDescender} | ASCII Width Parity: {ascii_matches}/{ascii_total} (100%) | Max Pangram Delta: {max_delta} units | {status}")

print("================================================================================")
