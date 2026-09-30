import urllib.request
import re
import os

repos = [
    'Healthcare-Analytics-Dashboard',
    '-Zomato-Analytics-Dashboard---Power-BI',
    'Credit-Card-Fraud-Detection',
    'OLA-Dashboard'
]

os.makedirs('assets', exist_ok=True)

for repo in repos:
    try:
        url = f'https://api.github.com/repos/jayzz98/{repo}/readme'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3.raw'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        images = re.findall(r'(https?://[^\s\"\'\)]+?\.(?:png|jpg|jpeg|gif))', html, re.IGNORECASE)
        if images:
            img_url = images[0]
            print(f'Found for {repo}: {img_url}')
            try:
                urllib.request.urlretrieve(img_url, f'assets/{repo}.png')
                print(f'Saved assets/{repo}.png')
            except Exception as e:
                print(f'Failed to download {img_url}: {e}')
        else:
            print(f'No image found in README for {repo}')
    except Exception as e:
        print(f'Error fetching README for {repo}: {e}')

# Download logos for client projects
logos = {
    'jnj': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Johnson_and_Johnson_Logo.svg/512px-Johnson_and_Johnson_Logo.svg.png',
    'wbd': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Warner_Bros._Discovery_logo.svg/512px-Warner_Bros._Discovery_logo.svg.png'
}

for name, url in logos.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(f'assets/{name}.png', 'wb') as out_file:
            out_file.write(response.read())
        print(f'Saved {name}.png')
    except Exception as e:
        print(f'Error downloading {name} logo: {e}')
