from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

user_font = TTFont(r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYREGULAR.OTF')
gen_font = TTFont('test_engine_regular.ttf')

user_cmap = user_font.getBestCmap()
gen_cmap = gen_font.getBestCmap()
user_hmtx = user_font['hmtx']
gen_hmtx = gen_font['hmtx']

common_cps = [cp for cp in user_cmap if cp in gen_cmap]
print(f"Total common codepoints: {len(common_cps)} / {len(user_cmap)}")

exact_w = sum(1 for cp in common_cps if user_hmtx[user_cmap[cp]][0] == gen_hmtx[gen_cmap[cp]][0])
exact_lsb = sum(1 for cp in common_cps if user_hmtx[user_cmap[cp]][1] == gen_hmtx[gen_cmap[cp]][1])

print(f"Advance width parity: {exact_w} / {len(common_cps)} ({exact_w/len(common_cps)*100:.2f}%)")
print(f"Left Side Bearing (LSB) parity: {exact_lsb} / {len(common_cps)} ({exact_lsb/len(common_cps)*100:.2f}%)")

# Test real text sentences
sample_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "Apple SF Pro Display Version 13.0d3e20 1:1 Alternative",
    "Design is not just what it looks like and feels like. Design is how it works.",
    "$1,234,567.89 (0123456789) + - * / = % @ # & !"
]

print("\n--- SENTENCE ADVANCE WIDTH TEST ---")
for t in sample_texts:
    w_user = sum(user_hmtx[user_cmap[ord(c)]][0] for c in t if ord(c) in user_cmap)
    w_gen = sum(gen_hmtx[gen_cmap[ord(c)]][0] for c in t if ord(c) in gen_cmap)
    diff = w_gen - w_user
    print(f"'{t[:30]}...': User={w_user} units, Gen={w_gen} units, Diff={diff} units")
