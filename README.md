# Album Covers

Cover art, one folder per album. 1024×1024 baseline JPEG (quality 92, 4:4:4
chroma, no alpha channel).

Gallery: <https://www.julienleveugle.com/album-covers/>

## Direct URLs

<!-- BEGIN ALBUMS -->

| Album | Artist | URL |
|---|---|---|
| Cue & Underscore | The Wolf Tone Ensemble | `https://www.julienleveugle.com/album-covers/Cue%20%26%20Underscore/cover.jpg` |
| Ground Control Lullabies | The Sputnik Cascades | `https://www.julienleveugle.com/album-covers/Ground%20Control%20Lullabies/cover.jpg` |
| Mademoiselle Tokyo | Nouvelle Ginza | `https://www.julienleveugle.com/album-covers/Mademoiselle%20Tokyo/cover.jpg` |
| Nine Nights | Vardlokk | `https://www.julienleveugle.com/album-covers/Nine%20Nights/cover.jpg` |
| Transmission 47 | Onde Spatiale | `https://www.julienleveugle.com/album-covers/Transmission%2047/cover.jpg` |
| Vorkurs Sessions | Dessau Drift | `https://www.julienleveugle.com/album-covers/Vorkurs%20Sessions/cover.jpg` |
| Yellow Monitor Dreams | Static Age | `https://www.julienleveugle.com/album-covers/Yellow%20Monitor%20Dreams/cover.jpg` |

<!-- END ALBUMS -->

Spaces in the folder names are percent-encoded as `%20`.

On the gallery page each card shows its full URL; click it to copy, or use
**Copy all URLs** to grab every one at once, newline-separated.

`https://julzkb.github.io/album-covers/…` also resolves, but issues a `301`
redirect to the custom domain above — use the custom-domain URLs directly for
anything that does not follow redirects.

## Adding an album

1. Create a folder named exactly as the album title.
2. Put `cover.jpg` in it (`.jpeg` and `.png` also work, but JPEG is preferred).
3. Put the artist name in `artist.txt` next to it.
4. Commit and push.

The `Build gallery` workflow runs `generate.py`, rebuilds `index.html` and the
table above from whatever folders exist, and commits the result. Nothing in
this README or the gallery page is maintained by hand.

To preview locally before pushing:

```bash
python3 generate.py
```

## Notes

The covers are also embedded in the corresponding FLAC files as `PICTURE`
blocks of type 3 (front cover). Baseline JPEG without an alpha channel is used
deliberately — RGBA PNG is silently ignored by VLC and several other players
even when the metadata block itself is valid.

Album art is AI-generated. The music is AI-generated with
[Stable Audio 3](https://github.com/Stability-AI/stable-audio-3); the artists
are fictional.
