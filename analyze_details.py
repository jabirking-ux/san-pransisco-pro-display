from fontTools.ttLib import TTFont

sf = TTFont('SF-Pro-Display-Regular-reference.otf')
ttf = TTFont('inter_extracted/extras/ttf/InterDisplay-Regular.ttf')

sf_cmap = sf.getBestCmap()
ttf_cmap = ttf.getBestCmap()

punct = ['.', ',', ':', ';', '!', '?', '(', ')', '[', ']', '{', '}', '"', "'", '`', '-', '—', '–', '/', '\\', '@', '#', '$', '%', '&', '*', '+', '=', '<', '>']
for p in punct:
    cp = ord(p)
    w_sf = sf['hmtx'][sf_cmap[cp]][0] if cp in sf_cmap else 'N/A'
    w_in = ttf['hmtx'][ttf_cmap[cp]][0] if cp in ttf_cmap else 'N/A'
    diff = w_in - w_sf if (w_sf != 'N/A' and w_in != 'N/A') else 'N/A'
    print(f"{repr(p):6s}: SF={str(w_sf):<6} Inter={str(w_in):<6} Diff={str(diff)}")
