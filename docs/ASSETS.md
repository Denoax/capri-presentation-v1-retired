# Original shapes. Literal evidence.

CAPRI's presentation uses independently authored angular lettering, flat green/magenta forms and one elastic displacement between held readable poses. These are conceptual illustrations, never product screenshots or live status. No image-generation model, third-party character art or external media input is used.

| Published asset | Purpose |
| --- | --- |
| `capri-hero-loop.gif` / `capri-hero-static.png` | 990×352 identity; name remains visible throughout |
| `workflow-loop.gif` / `workflow-static.png` | 990×240 conceptual roles and final human decision |
| `capri-divider-loop.gif` / `capri-divider-static.png` | 990×24 restrained line motif |
| `capri-social-1280x640.png` | 1280×640 opaque social composition |
| `capri-hero.svg` / `workflow.svg` | Editable original vector sources |

Files live in [showcase/capri](../showcase/capri). [MEDIA.json](../showcase/capri/MEDIA.json) records exact dimensions, durations, frame counts, weights and hashes. [BUILD.json](../showcase/capri/BUILD.json) records Pillow/font identities. Original sources: [media renderer](../scripts/build_capri_media.py). Original geometry and presentation: Mani Marami Milani's CAPRI project. License selection remains pending; no third-party-art license is asserted.

## Rebuild

Use a separate environment; media dependencies do not alter the controller lock.

```sh
python3 -m venv .media-venv
. .media-venv/bin/activate
python -m pip install -r requirements-media.txt
python scripts/build_capri_media.py --font /path/to/NotoSansMono-Regular.ttf
python scripts/check_presentation.py
```

Use the Noto Sans Mono font bytes whose SHA-256 is recorded in BUILD.json and the pinned Pillow version for byte-reproducible raster output. The font is an external build input, not bundled; obtain it from [Noto's original source](https://github.com/notofonts/latin-greek-cyrillic). SVG text uses the viewer's monospace font and may differ; CAPRI's display lettering is geometry. Static PNGs preserve the exported composition. Rebuild MEDIA.json with `check_presentation.py` after rendering.

## Design sources

The supplied authored kit is the implementation base. Character excerpts were inspected privately for flat opposing green/magenta colors, angular negative space and held/elastic motion; those reference files are excluded. Tokens are sampled working choices, not official studio swatches. No character portrait is traced or synthesized.

[Mani's portfolio](https://github.com/Denoax/portfolio) contributes the wide motion-led opening and concise native-text introduction. [Kona Desktop](https://github.com/Denoax/konata-hyprland-dotfiles) contributes a coherent canvas/palette and useful setup/status documentation. Their media and prose are not copied into CAPRI. Original reference authors retain their rights.

GitHub controls GIF autoplay. The hero links to the [complete static README](README_STATIC.md); static first frames retain identity and all important explanations are native text. GIFs do not implement an independent reduced-motion switch. A committed social PNG is only a candidate until the actual repository setting is uploaded and verified.
