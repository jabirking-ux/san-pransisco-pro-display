from fontTools.ttLib import TTFont

ref = TTFont('references/SF-Pro-Display-Regular.otf')
gen = TTFont('dist/ttf/SanPransiscoProDisplay-Regular.ttf')

print("Ref tables:", list(ref.keys()))
print("Gen tables:", list(gen.keys()))

def inspect_kern(f, name):
    print(f"\n--- {name} GPOS ---")
    if 'GPOS' not in f:
        print("No GPOS table!")
        return
    gpos = f['GPOS'].table
    features = [rec.FeatureTag for rec in gpos.FeatureList.FeatureRecord]
    print("Features:", features)

inspect_kern(ref, "SF Pro Display")
inspect_kern(gen, "San Pransisco Pro Display")
