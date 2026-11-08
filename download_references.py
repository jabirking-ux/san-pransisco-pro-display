import urllib.request, os

weights = [
    'Regular', 'Medium', 'Semibold', 'Bold', 'Black', 'Light', 'Thin', 'Ultralight', 'Heavy'
]
base_url = 'https://raw.githubusercontent.com/sahibjotsaggu/San-Francisco-Pro-Fonts/master/'
os.makedirs('references', exist_ok=True)

for w in weights:
    filename = f'SF-Pro-Display-{w}.otf'
    target_path = os.path.join('references', filename)
    if not os.path.exists(target_path):
        url = base_url + filename
        print(f'Downloading {filename}...')
        try:
            urllib.request.urlretrieve(url, target_path)
            print(f'  Saved to {target_path}')
        except Exception as e:
            print(f'  Failed: {e}')
    else:
        print(f'{filename} already cached')
