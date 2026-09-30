import urllib.request
import json
import os

repos = [
    'Healthcare-Analytics-Dashboard',
    '-Zomato-Analytics-Dashboard---Power-BI',
    'Credit-Card-Fraud-Detection',
    'OLA-Dashboard',
    'HR-Data-Analytics'
]

os.makedirs('assets', exist_ok=True)

for repo in repos:
    try:
        url = f'https://api.github.com/repos/jayzz98/{repo}/contents'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req).read().decode('utf-8')
        contents = json.loads(response)
        for item in contents:
            if item['name'].endswith(('.png', '.jpg', '.jpeg', '.gif')):
                print(f'Found image in {repo}: {item["name"]}')
                img_url = item['download_url']
                try:
                    req_img = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req_img) as response_img, open(f'assets/{repo}.png', 'wb') as out_file:
                        out_file.write(response_img.read())
                    print(f'Saved assets/{repo}.png')
                    break # Just grab the first one
                except Exception as e:
                    print(f'Failed to download {img_url}: {e}')
    except Exception as e:
        print(f'Error fetching contents for {repo}: {e}')

# Working logos
logos = {
    'jnj': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Johnson_and_Johnson_Logo.svg/1024px-Johnson_and_Johnson_Logo.svg.png',
    'wbd': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Warner_Bros._Discovery_logo.svg/1024px-Warner_Bros._Discovery_logo.svg.png'
}

for name, url in logos.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(f'assets/{name}.png', 'wb') as out_file:
            out_file.write(response.read())
        print(f'Saved {name}.png')
    except Exception as e:
        print(f'Error downloading {name} logo: {e}')
