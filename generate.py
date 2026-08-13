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
        albums.append({"album": d.name, "artist": artist, "cover": cover,
                       "path": f"{quote(d.name)}/{quote(cover)}"})
    return albums


FIGURE = """    <figure>
      <img src="{path}" alt="{alt} cover" loading="lazy" width="1024" height="1024">
      <figcaption>
        <div class="album">{album}</div>
        <div class="artist">{artist}</div>
        <code>{path}</code>
      </figcaption>
    </figure>"""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Album Covers</title>
<style>
  :root {{
    --bg: #fbfbf9; --fg: #1a1a1a; --muted: #6b6b6b;
    --card: #ffffff; --line: #e4e4e0;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #141414; --fg: #ececec; --muted: #9a9a9a;
            --card: #1d1d1d; --line: #2e2e2e; }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 3rem 1.5rem; background: var(--bg); color: var(--fg);
    font: 16px/1.6 ui-sans-serif, -apple-system, "Helvetica Neue", sans-serif;
  }}
  main {{ max-width: 1100px; margin: 0 auto; }}
  h1 {{ font-size: 1.4rem; font-weight: 650; margin: 0 0 .3rem; letter-spacing: -.01em; }}
  .sub {{ color: var(--muted); font-size: .9rem; margin: 0 0 2.5rem; }}
  .grid {{ display: grid; gap: 2rem; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }}
  figure {{ margin: 0; background: var(--card); border: 1px solid var(--line);
           border-radius: 10px; overflow: hidden; }}
  img {{ display: block; width: 100%; height: auto; aspect-ratio: 1; object-fit: cover; }}
  figcaption {{ padding: .9rem 1rem 1rem; }}
  .album {{ font-weight: 600; font-size: .95rem; }}
  .artist {{ color: var(--muted); font-size: .85rem; margin-top: .1rem; }}
  code {{ display: block; margin-top: .7rem; padding: .5rem .6rem; font-size: .72rem;
         background: var(--bg); border: 1px solid var(--line); border-radius: 6px;
         overflow-x: auto; white-space: nowrap; font-family: ui-monospace, monospace; }}
</style>
</head>
<body>
<main>
  <h1>Album Covers</h1>
  <p class="sub">{count} album{plural}, 1024&times;1024 JPEG. Direct links below each cover.</p>
  <div class="grid">

{figures}

  </div>
</main>
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
        FIGURE.format(path=a["path"], alt=html.escape(a["album"], quote=True),
                      album=html.escape(a["album"]), artist=html.escape(a["artist"]))
        for a in albums
    )
    page = PAGE.format(count=len(albums), plural="" if len(albums) == 1 else "s",
                       figures=figures)
    (ROOT / "index.html").write_text(page, encoding="utf-8")

    rows = "\n".join(
        f'| {a["album"]} | {a["artist"]} | `{BASE_URL}/{a["path"]}` |' for a in albums
    )
    table = (f"{START}\n\n| Album | Artist | URL |\n|---|---|---|\n{rows}\n\n{END}")

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
