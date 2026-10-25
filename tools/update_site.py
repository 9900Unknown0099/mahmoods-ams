#!/usr/bin/env python3
"""
Keeps the website in sync with the APKs in /downloads.

Naming rule:   downloads/Mahmoods-AMS-v1.0.apk, Mahmoods-AMS-v1.1.apk, Mahmoods-AMS-v1.2.apk ...
  * The HIGHEST version is the main "Download" button.
  * Every other version is listed automatically under "Previous versions".
Optional release notes: put a text file next to the APK with the same name,
  e.g. downloads/Mahmoods-AMS-v1.1.txt  (one change per line).

Run:  python3 tools/update_site.py     (the GitHub Action does this for you on every upload)
"""
import glob, hashlib, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = os.path.join(ROOT, "downloads")
NAME = re.compile(r"^Mahmoods-AMS-v(\d+(?:\.\d+)*)\.apk$")
ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" width="18" height="18"><path d="M12 3v12m0 0l-5-5m5 5l5-5M4 20h16"/></svg>'

def vkey(v): return tuple(int(x) for x in v.split("."))

rels = []
for p in glob.glob(os.path.join(DL, "*.apk")):
    m = NAME.match(os.path.basename(p))
    if not m:
        print(f"Skipping {os.path.basename(p)} (name must look like Mahmoods-AMS-v1.1.apk)")
        continue
    v = m.group(1)
    notes_path = os.path.join(DL, f"Mahmoods-AMS-v{v}.txt")
    notes = []
    if os.path.exists(notes_path):
        notes = [ln.strip(" -*\t") for ln in open(notes_path, encoding="utf-8").read().splitlines() if ln.strip()]
    data = open(p, "rb").read()
    rels.append(dict(v=v, key=vkey(v), file=os.path.basename(p), mb=len(data) / 1048576,
                     sha=hashlib.sha256(data).hexdigest(), notes=notes))
if not rels:
    sys.exit("No APK found in downloads/ named like Mahmoods-AMS-v1.0.apk")
rels.sort(key=lambda r: r["key"], reverse=True)
latest, previous = rels[0], rels[1:]

def li(items): return "".join(f"<li>{html.escape(n)}</li>" for n in items)

# ---- generated blocks ----
notes_block = ""
if latest["notes"]:
    notes_block = (f'<div class="notes rv"><h3>What&rsquo;s new in {latest["v"]}</h3>'
                   f'<ul class="checks">{li(latest["notes"])}</ul></div>')
prevlink = '<a class="link" href="#previous">Previous versions &rsaquo;</a>' if previous else ""
prev_block = ""
if previous:
    rows = ""
    for i, r in enumerate(previous):
        n = f"<ul>{li(r['notes'])}</ul>" if r["notes"] else ""
        rows += (f'<article class="ver"><div class="ver-main"><b>Version {r["v"]}</b><span>{r["mb"]:.1f} MB</span></div>'
                 f'<a class="btn btn-dark" href="downloads/{r["file"]}" download>{ICON}Download</a>{n}'
                 f'<div class="ver-hash">SHA-256 <span class="hash" id="sha-{i}">{r["sha"]}</span> '
                 f'<button class="copy" data-copy="#sha-{i}">Copy</button></div></article>')
    prev_block = ('<section class="sec mist" id="previous" data-nav="light"><div class="narrow">'
                  '<p class="eyebrow rv">Earlier releases</p>'
                  '<h2 class="h2 split grad-dark" style="font-size:clamp(32px,4.6vw,58px)">Previous versions.</h2>'
                  '<p class="body rv" style="margin-top:14px">Need an older build? Every earlier release stays available. '
                  'The latest version is recommended &mdash; it has the newest fixes.</p>'
                  f'<div class="ver-list rv">{rows}</div></div></section>')
blocks = {"NOTES": notes_block, "PREVLINK": prevlink, "PREVIOUS": prev_block}

def ensure_markers(text):
    """Re-insert the auto-managed block markers if a hand edit or an older page copy lost them."""
    if "PREVLINK:START" not in text:
        text = re.sub(r'(<a class="link" href="#install">How to install &rsaquo;</a>)', r'\1<!-- PREVLINK:START --><!-- PREVLINK:END -->', text, count=1)
    if "NOTES:START" not in text:
        text = re.sub(r'(</table>)(\s*<p class="body rv" style="margin-top:22px">To verify)', r'\1\n<!-- NOTES:START --><!-- NOTES:END -->\2', text, count=1)
    if "PREVIOUS:START" not in text:
        text = text.replace('<footer class="footer"', '<!-- PREVIOUS:START --><!-- PREVIOUS:END -->\n<footer class="footer"', 1)
    return text

def patch(text):
    holders = {}
    if text.lstrip().startswith("<!DOCTYPE") and "id=\"sha\"" in text:
        text = ensure_markers(text)
    for k in blocks:
        text, n = re.subn(rf"<!-- {k}:START -->.*?<!-- {k}:END -->", f"@@{k}@@", text, flags=re.S)
        holders[k] = n
    text = re.sub(r"Mahmoods-AMS-v\d+(?:\.\d+)*\.apk", latest["file"], text)
    text = re.sub(r"Version \d+(?:\.\d+)*", f"Version {latest['v']}", text)
    text = re.sub(r"(?<![\w-])v\d+(?:\.\d+)+(?![\w.])", f"v{latest['v']}", text)
    text = re.sub(r'data-count="[\d.]+"(?= data-suffix=" MB")', f'data-count="{latest["mb"]:.1f}"', text)
    text = re.sub(r"\d+\.\d MB", f"{latest['mb']:.1f} MB", text)
    text = re.sub(r'(<span class="hash" id="sha">)[0-9a-f]{64}(</span>)', rf"\g<1>{latest['sha']}\g<2>", text)
    text = re.sub(r"(<span>Version</span><b>)[^<]*", rf"\g<1>{latest['v']}", text)
    text = re.sub(r"(<th>Version</th><td>)[^<]*", rf"\g<1>{latest['v']}", text)
    for k, content in blocks.items():
        text = text.replace(f"@@{k}@@", f"<!-- {k}:START -->{content}<!-- {k}:END -->")
    return text

for page in glob.glob(os.path.join(ROOT, "*.html")):
    old = open(page, encoding="utf-8").read()
    new = patch(old)
    if new != old:
        open(page, "w", encoding="utf-8").write(new)
        print("Updated", os.path.basename(page))

# version.json is what the installed APP reads to learn that a newer version exists.
with open(os.path.join(ROOT, "version.json"), "w", encoding="utf-8") as f:
    json.dump({"versionName": latest["v"], "apkUrl": "downloads/" + latest["file"], "pageUrl": "download.html",
               "notes": latest["notes"], "sha256": latest["sha"]}, f, indent=2)
print("Wrote version.json")

print(f"\nLatest: v{latest['v']} ({latest['mb']:.1f} MB)  SHA-256 {latest['sha']}")
print("Previous:", ", ".join("v" + r["v"] for r in previous) or "none")
