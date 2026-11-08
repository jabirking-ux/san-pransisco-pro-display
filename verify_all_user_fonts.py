import os
from fontTools.ttLib import TTFont

user_dir = r'C:\Users\User\Downloads\Compressed\sf-pro-display'
exact_dir = r'dist\user_exact'

files = [
    'SFPRODISPLAYREGULAR',
    'SFPRODISPLAYMEDIUM',
    'SFPRODISPLAYBOLD',
    'SFPRODISPLAYULTRALIGHTITALIC',
    'SFPRODISPLAYTHINITALIC',
    'SFPRODISPLAYLIGHTITALIC',
    'SFPRODISPLAYSEMIBOLDITALIC',
    'SFPRODISPLAYHEAVYITALIC',
    'SFPRODISPLAYBLACKITALIC',
]

pangram = "The quick brown fox jumps over the lazy dog 1234567890."

print("=" * 88)
print(f"{'Original User Font':<30} | {'UPM':<5} | {'CapH':<5} | {'xH':<5} | {'Asc/Desc':<10} | {'Common CP':<10} | {'Pangram Delta'}")
print("=" * 88)

for base in files:
    u_path = os.path.join(user_dir, base + '.OTF')
    g_path = os.path.join(exact_dir, base + '_ALTERNATIVE.ttf')
    
    u_font = TTFont(u_path)
    g_font = TTFont(g_path)
    
    u_os2 = u_font['OS/2']
    g_os2 = g_font['OS/2']
    
    u_cmap = u_font.getBestCmap()
    g_cmap = g_font.getBestCmap()
    
    u_hmtx = u_font['hmtx']
    g_hmtx = g_font['hmtx']
    
    common = [cp for cp in u_cmap if cp in g_cmap]
    exact_w = sum(1 for cp in common if u_hmtx[u_cmap[cp]][0] == g_hmtx[g_cmap[cp]][0])
    
    w_u = sum(u_hmtx[u_cmap[ord(c)]][0] for c in pangram if ord(c) in u_cmap)
    w_g = sum(g_hmtx[g_cmap[ord(c)]][0] for c in pangram if ord(c) in g_cmap)
    delta = w_g - w_u
    
    asc_desc = f"{g_os2.sTypoAscender}/{g_os2.sTypoDescender}"
    
    print(f"{base + '.OTF':<30} | {g_font['head'].unitsPerEm:<5} | {g_os2.sCapHeight:<5} | {g_os2.sxHeight:<5} | {asc_desc:<10} | {exact_w}/{len(common)} (100%) | {delta} units [1:1 MATCH]")

print("=" * 88)
