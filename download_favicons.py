import urllib.request

jnj_url = "https://www.google.com/s2/favicons?domain=jnj.com&sz=128"
wbd_url = "https://www.google.com/s2/favicons?domain=wbd.com&sz=128"

req_jnj = urllib.request.Request(jnj_url, headers={'User-Agent': 'Mozilla/5.0'})
req_wbd = urllib.request.Request(wbd_url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req_jnj) as response, open('assets/jnj_icon.png', 'wb') as f:
    f.write(response.read())

with urllib.request.urlopen(req_wbd) as response, open('assets/wbd_icon.png', 'wb') as f:
    f.write(response.read())

print("Downloaded favicons successfully!")
