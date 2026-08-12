# Album Covers

Cover art for three albums, one folder per album. 1024×1024 baseline JPEG
(quality 92, 4:4:4 chroma, no alpha channel).

Gallery: <https://julzkb.github.io/album-covers/>

## Direct URLs

| Album | Artist | URL |
|---|---|---|
| Ground Control Lullabies | The Sputnik Cascades | `https://julzkb.github.io/album-covers/Ground%20Control%20Lullabies/cover.jpg` |
| Transmission 47 | Onde Spatiale | `https://julzkb.github.io/album-covers/Transmission%2047/cover.jpg` |
| Vorkurs Sessions | Dessau Drift | `https://julzkb.github.io/album-covers/Vorkurs%20Sessions/cover.jpg` |

Spaces in the folder names are percent-encoded as `%20` in URLs.

## Notes

The covers are also embedded directly in the FLAC files as `PICTURE` blocks of
type 3 (front cover). Baseline JPEG without an alpha channel is used
deliberately — RGBA PNG is silently ignored by VLC and several other players
even when the metadata block itself is valid.

Album art is AI-generated. The music is AI-generated with
[Stable Audio 3](https://github.com/Stability-AI/stable-audio-3); the artists
are fictional.
