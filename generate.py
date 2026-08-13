#!/usr/bin/env python3
"""Regenerate index.html and the README URL table from the folder structure.

An album is any top-level directory containing a cover image. The directory
name is the album title; the artist is read from an optional `artist.txt`
inside it. Adding an album is therefore: make the folder, drop in a cover
(and an artist.txt), push. CI runs this and commits the result.

Run locally with:  python3 generate.py
"""

from pathlib import Path
from urllib.parse import quote
import html
import re
import sys

ROOT = Path(__file__).parent
BASE_URL = "https://www.julienleveugle.com/album-covers"
COVER_NAMES = ("cover.jpg", "cover.jpeg", "cover.png")


def find_albums():
    """Every top-level dir holding a cover image, sorted by album title."""
    albums = []
    for d in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
        if not d.is_dir() or d.name.startswith((".", "_")):
            continue
        cover = next((n for n in COVER_NAMES if (d / n).is_file()), None)
        if not cover:
            continue
        artist_file = d / "artist.txt"
        artist = artist_file.read_text(encoding="utf-8").strip() if artist_file.is_file() else ""
        rel = f"{quote(d.name)}/{quote(cover)}"
        albums.append({"album": d.name, "artist": artist, "cover": cover,
                       "rel": rel, "url": f"{BASE_URL}/{rel}"})
    return albums


# NOTE: templates use __PLACEHOLDER__ tokens and str.replace rather than
# str.format, so the CSS and JS braces below need no escaping.

FIGURE = """    <figure>
      <a class="shot" href="__REL__" target="_blank" rel="noopener">
        <img src="__REL__" alt="__ALT__ cover" loading="lazy" width="1024" height="1024">
      </a>
      <figcaption>
        <div class="album">__ALBUM__</div>
        <div class="artist">__ARTIST__</div>
        <button class="copy" type="button" data-url="__URL__">
          <span class="url">__URL__</span>
          <span class="hint" aria-hidden="true">Copy</span>
        </button>
      </figcaption>
    </figure>"""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Album Covers</title>
<style>
  :root {
    --bg: #fbfbf9; --fg: #1a1a1a; --muted: #6b6b6b;
    --card: #ffffff; --line: #e4e4e0; --ok: #1c7c4a; --okbg: #e8f5ee;
  }
  @media (prefers-color-scheme: dark) {
    :root { --bg: #141414; --fg: #ececec; --muted: #9a9a9a;
            --card: #1d1d1d; --line: #2e2e2e; --ok: #6ede9f; --okbg: #16301f; }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 3rem 1.5rem; background: var(--bg); color: var(--fg);
    font: 16px/1.6 ui-sans-serif, -apple-system, "Helvetica Neue", sans-serif;
  }
  main { max-width: 1100px; margin: 0 auto; }
  h1 { font-size: 1.4rem; font-weight: 650; margin: 0 0 .3rem; letter-spacing: -.01em; }
  .sub { color: var(--muted); font-size: .9rem; margin: 0 0 1.5rem; }
  .bar { margin: 0 0 2.5rem; }
  .grid { display: grid; gap: 2rem; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }
  figure { margin: 0; background: var(--card); border: 1px solid var(--line);
           border-radius: 10px; overflow: hidden; }
  .shot { display: block; }
  img { display: block; width: 100%; height: auto; aspect-ratio: 1; object-fit: cover; }
  figcaption { padding: .9rem 1rem 1rem; }
  .album { font-weight: 600; font-size: .95rem; }
  .artist { color: var(--muted); font-size: .85rem; margin-top: .1rem; }

  button { font: inherit; color: inherit; cursor: pointer; }
  .copy {
    display: flex; align-items: flex-start; gap: .6rem; width: 100%; text-align: left;
    margin-top: .7rem; padding: .55rem .6rem; background: var(--bg);
    border: 1px solid var(--line); border-radius: 6px; transition: border-color .15s;
  }
  .copy:hover { border-color: var(--muted); }
  /* Wrap rather than truncate: the whole point is showing the full URL, and
     the album title is already on the card so a truncated tail adds nothing. */
  .copy .url {
    flex: 1; min-width: 0; font-size: .68rem; line-height: 1.45;
    word-break: break-all; text-align: left;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--muted);
  }
  .copy .hint { flex: none; margin-top: .1rem; font-size: .62rem; font-weight: 700;
                letter-spacing: .05em; text-transform: uppercase; color: var(--muted); }
  .copy.done { border-color: var(--ok); background: var(--okbg); }
  .copy.done .hint, .copy.done .url { color: var(--ok); }

  .copyall {
    padding: .45rem .8rem; background: var(--card); border: 1px solid var(--line);
    border-radius: 6px; font-size: .82rem;
  }
  .copyall:hover { border-color: var(--muted); }
  .copyall.done { border-color: var(--ok); background: var(--okbg); color: var(--ok); }
</style>
</head>
<body>
<main>
  <h1>Album Covers</h1>
  <p class="sub">__COUNT__ album__PLURAL__, 1024&times;1024 JPEG. Click a URL to copy it.</p>
  <p class="bar"><button class="copyall" type="button">Copy all URLs</button></p>
  <div class="grid">

__FIGURES__

  </div>
</main>
<script>
// Clipboard API needs a secure context. The canonical host is HTTPS, but the
// julzkb.github.io alias redirects to http://, so keep a legacy fallback.
async function copyText(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch (e) { /* fall through */ }
  try {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:absolute;left:-9999px;top:0';
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand('copy');
    document.body.removeChild(ta);
    return ok;
  } catch (e) { return false; }
}

function flash(btn, label) {
  const hint = btn.querySelector('.hint') || btn;
  const original = hint.textContent;
  hint.textContent = label;
  btn.classList.add('done');
  clearTimeout(btn._t);
  btn._t = setTimeout(() => {
    hint.textContent = original;
    btn.classList.remove('done');
  }, 1400);
}

document.querySelectorAll('.copy').forEach(btn => {
  btn.addEventListener('click', async () => {
    flash(btn, (await copyText(btn.dataset.url)) ? 'Copied' : 'Failed');
  });
});

const all = document.querySelector('.copyall');
if (all) {
  const urls = [...document.querySelectorAll('.copy')].map(b => b.dataset.url).join('\\n');
  all.addEventListener('click', async () => {
    const ok = await copyText(urls);
    all.textContent = ok ? 'Copied all URLs' : 'Copy failed';
    all.classList.add('done');
    clearTimeout(all._t);
    all._t = setTimeout(() => {
      all.textContent = 'Copy all URLs';
      all.classList.remove('done');
    }, 1400);
  });
}
</script>
</body>
</html>
"""

START, END = "<!-- BEGIN ALBUMS -->", "<!-- END ALBUMS -->"


def main():
    albums = find_albums()
    if not albums:
        print("no albums found", file=sys.stderr)
        return 1

    figures = "\n\n".join(
        FIGURE.replace("__REL__", a["rel"])
              .replace("__URL__", a["url"])
              .replace("__ALT__", html.escape(a["album"], quote=True))
              .replace("__ALBUM__", html.escape(a["album"]))
              .replace("__ARTIST__", html.escape(a["artist"]))
        for a in albums
    )
    page = (PAGE.replace("__FIGURES__", figures)
                .replace("__COUNT__", str(len(albums)))
                .replace("__PLURAL__", "" if len(albums) == 1 else "s"))
    (ROOT / "index.html").write_text(page, encoding="utf-8")

    rows = "\n".join(f'| {a["album"]} | {a["artist"]} | `{a["url"]}` |' for a in albums)
    table = f"{START}\n\n| Album | Artist | URL |\n|---|---|---|\n{rows}\n\n{END}"

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    if START in readme and END in readme:
        readme = re.sub(f"{re.escape(START)}.*?{re.escape(END)}", lambda _: table,
                        readme, flags=re.S)
        readme_path.write_text(readme, encoding="utf-8")
    else:
        print(f"warning: {START}/{END} markers missing in README.md — table not updated",
              file=sys.stderr)

    for a in albums:
        print(f"  {a['album']}  —  {a['artist'] or '(no artist.txt)'}")
    print(f"\n  wrote index.html and README.md for {len(albums)} albums")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
