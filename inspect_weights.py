import urllib.request, os
from fontTools.ttLib import TTFont

weights = [
    'SF-Pro-Display-Regular.otf',
    'SF-Pro-Display-Bold.otf',
    'SF-Pro-Display-Medium.otf',
    'SF-Pro-Display-Semibold.otf'
]
base_url = 'https://raw.githubusercontent.com/sahibjotsaggu/San-Francisco-Pro-Fonts/master/'

for w in weights:
    local_path = f'ref_{w}'
    if not os.path.exists(local_path):
        print(f'Fetching {w}...')
        try:
            urllib.request.urlretrieve(base_url + w, local_path)
        except Exception as e:
            print(f'Failed to fetch {w}:', e)
            continue
    f = TTFont(local_path)
    os2 = f['OS/2']
    hhea = f['hhea']
    print(f"{w}: UPM={f['head'].unitsPerEm}, Weight={os2.usWeightClass}, CapH={os2.sCapHeight}, xH={os2.sxHeight}, Asc={os2.sTypoAscender}, Desc={os2.sTypoDescender}")
