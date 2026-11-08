import os
import zipfile

os.makedirs('releases', exist_ok=True)

# 1. TTF Package
with zipfile.ZipFile('releases/SanPransiscoProDisplay-TTF.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir('dist/ttf'):
        if f.endswith('.ttf'):
            z.write(os.path.join('dist/ttf', f), f)
    z.write('OFL.txt', 'OFL.txt')
    z.write('README.md', 'README.md')
print("Created releases/SanPransiscoProDisplay-TTF.zip")

# 2. WOFF2 Package
with zipfile.ZipFile('releases/SanPransiscoProDisplay-WOFF2.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir('dist/woff2'):
        if f.endswith('.woff2'):
            z.write(os.path.join('dist/woff2', f), f)
    z.write('san-pransisco.css', 'san-pransisco.css')
    z.write('OFL.txt', 'OFL.txt')
print("Created releases/SanPransiscoProDisplay-WOFF2.zip")

# 3. 1:1 Master Drop-ins Package
with zipfile.ZipFile('releases/SanPransiscoProDisplay-1-to-1-Dropins.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir('dist/user_exact'):
        z.write(os.path.join('dist/user_exact', f), f)
    z.write('OFL.txt', 'OFL.txt')
print("Created releases/SanPransiscoProDisplay-1-to-1-Dropins.zip")

# 4. Complete Package
with zipfile.ZipFile('releases/SanPransiscoProDisplay-Complete.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk('dist'):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, '.')
            z.write(full, rel)
    z.write('san-pransisco.css', 'san-pransisco.css')
    z.write('specimen.html', 'specimen.html')
    z.write('OFL.txt', 'OFL.txt')
    z.write('README.md', 'README.md')
print("Created releases/SanPransiscoProDisplay-Complete.zip")
