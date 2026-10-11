#!/usr/bin/env python3
"""After replacing the APK in /downloads, run:  python3 tools/update_checksum.py
Recomputes the SHA-256 and file size and patches download.html + index.html."""
import glob, hashlib, os, re, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
apks = glob.glob(os.path.join(root, "downloads", "*.apk"))
if len(apks) != 1:
    sys.exit(f"Expected exactly one .apk in downloads/, found {len(apks)}")
apk = apks[0]
sha = hashlib.sha256(open(apk, "rb").read()).hexdigest()
mb = os.path.getsize(apk) / (1024 * 1024)
name = os.path.basename(apk)
p = os.path.join(root, "download.html")
s = open(p, encoding="utf-8").read()
s = re.sub(r'(<span class="hash" id="sha">)[0-9a-f]{64}(</span>)', rf'\g<1>{sha}\g<2>', s)
s = re.sub(r'downloads/[^"]+\.apk', f"downloads/{name}", s)
s = re.sub(r'\d+\.\d MB', f"{mb:.1f} MB", s)
open(p, "w", encoding="utf-8").write(s)
q = os.path.join(root, "index.html")
t = open(q, encoding="utf-8").read()
t = re.sub(r'data-count="[\d.]+" data-suffix=" MB"', f'data-count="{mb:.1f}" data-suffix=" MB"', t)
t = re.sub(r'\d+\.\d MB', f"{mb:.1f} MB", t)
open(q, "w", encoding="utf-8").write(t)
print(f"Updated: {name}  {mb:.1f} MB\nSHA-256: {sha}\nIf the version number changed, also edit 'Version 1.0' text in download.html, index.html and about.html.")
