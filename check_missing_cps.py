from fontTools.ttLib import TTFont

user_font = TTFont(r'C:\Users\User\Downloads\Compressed\sf-pro-display\SFPRODISPLAYREGULAR.OTF')
gen_font = TTFont('test_engine_regular.ttf')

user_cmap = user_font.getBestCmap()
gen_cmap = gen_font.getBestCmap()

missing = [cp for cp in user_cmap if cp not in gen_cmap]
print(f"Missing codepoints count: {len(missing)}")
for cp in missing[:30]:
    print(f"U+{cp:04X} ({chr(cp) if cp < 65536 else '?'}) -> {user_cmap[cp]}")
