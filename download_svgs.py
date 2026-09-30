import urllib.request
import os

jnj_url = "https://upload.wikimedia.org/wikipedia/commons/b/b3/Johnson_and_Johnson_Logo.svg"
wbd_url = "https://upload.wikimedia.org/wikipedia/commons/2/25/Warner_Bros._Discovery_logo.svg"

req_jnj = urllib.request.Request(jnj_url, headers={'User-Agent': 'Mozilla/5.0'})
req_wbd = urllib.request.Request(wbd_url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req_jnj) as response, open('assets/jnj.svg', 'wb') as f:
    f.write(response.read())

with urllib.request.urlopen(req_wbd) as response, open('assets/wbd.svg', 'wb') as f:
    f.write(response.read())

print("Downloaded SVGs successfully!")
