#!/usr/bin/env python3
"""Export original geometric CAPRI lettering and motion. No external art input."""
from pathlib import Path
import argparse
import hashlib
import json
import math

INK = '#110821'
PINK = '#E40F66'
GREEN = '#27FB86'
WHITE = '#FEFEFF'
VIOLET = '#5129A9'
MUTED = '#B9AFC9'
FONT_PATH = None

# Original angular letter outlines, not traced from the anime title or character.
LETTERS = {
 'C': [[(88,0),(16,0),(0,16),(0,124),(16,140),(88,140),(88,110),(32,110),(32,30),(88,30)]],
 'A': [[(0,140),(30,0),(64,0),(94,140),(63,140),(57,108),(36,108),(30,140)],
       [(41,80),(52,80),(46,45)]],
 'P': [[(0,140),(0,0),(73,0),(91,18),(91,72),(73,90),(31,90),(31,140)],
       [(31,29),(60,29),(60,60),(31,60)]],
 'R': [[(0,140),(0,0),(73,0),(91,18),(91,72),(72,90),(96,140),(61,140),(39,90),(31,90),(31,140)],
       [(31,29),(60,29),(60,60),(31,60)]],
 'I': [[(0,0),(71,0),(71,28),(52,28),(52,112),(71,112),(71,140),(0,140),(0,112),(19,112),(19,28),(0,28)]]
}


def polys_letter(letter, x, y, scale):
    return [[(x+px*scale,y+py*scale) for px,py in points] for points in LETTERS[letter]]


def pulse(phase):
    """One elastic displacement between long, readable held poses."""
    keys = [(0, 0), (.32, 0), (.39, 1), (.44, -.32), (.50, .13), (.60, 0), (1, 0)]
    for (start, a), (end, z) in zip(keys, keys[1:]):
        if start <= phase <= end:
            t = (phase - start) / (end - start)
            return a + (z - a) * t * t * (3 - 2 * t)
    return 0


def geometry(phase=0):
    shapes = []
    x = 44
    for letter in 'CAPRI':
        for i, points in enumerate(polys_letter(letter,x,91,1.05)):
            shapes.append((points,WHITE if i==0 else INK))
        x += 112
    # A narrow editorial cut across the lettering, with original detached shards.
    shapes.append(([(44,170),(601,156),(601,163),(44,177)],INK))
    shapes.append(([(80,233),(595,220),(594,227),(80,240)],PINK))
    # Three nested angular C-forms suggest the three scoped roles; no character silhouette.
    for i in range(3):
        scale = (1.64,1.17,.70)[i]
        x = 718 + i*16 + pulse(phase)*11*(1-i*.18)
        y = 78 + i*28
        pts=polys_letter('C',x,y,scale)[0]
        pts=[(x+(px-x)*(1+.05*pulse(phase)), y+(py-y)*(1-.025*pulse(phase))) for px,py in pts]
        shapes.append((pts,(GREEN,PINK,VIOLET)[i]))
    shapes.extend([
        ([(660,48),(678,48),(660,86)],PINK),
        ([(949,268),(949,229),(930,268)],GREEN),
        ([(884,45),(923,45),(912,58),(873,58)],PINK)
    ])
    return shapes


def svg(phase=0):
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="990" height="352" viewBox="0 0 990 352" role="img" aria-labelledby="title desc">',
           '<title id="title">CAPRI — Three sessions. One contract.</title>',
           '<desc id="desc">Original green and magenta geometric wordmark for the experimental native Codex workflow. Abstract illustration, not application footage.</desc>',
           '<rect width="990" height="352" fill="'+INK+'"/>']
    for points,fill in geometry(phase):
        parts.append('<polygon fill="'+fill+'" points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in points)+'"/>')
    parts.extend([
      '<g fill="'+MUTED+'" font-family="monospace" font-size="12"><text x="45" y="40">NATIVE CODEX WORKFLOW</text></g>',
      '<text x="45" y="274" fill="'+WHITE+'" font-family="monospace" font-size="19">THREE SESSIONS. ONE CONTRACT.</text>',
      '<g fill="'+MUTED+'" font-family="monospace" font-size="11"><text x="45" y="317">THINKER</text><text x="181" y="317">DOER</text><text x="305" y="317">REVIEWER</text><text x="694" y="40">RESEARCH / BUILD / REVIEW</text></g>',
      '<path d="M108 313H163M222 313H287" stroke="'+VIOLET+'" stroke-width="2"/>',
      '</svg>'
    ])
    return '\n'.join(parts)+'\n'


def font(size):
    from PIL import ImageFont
    return ImageFont.truetype(str(FONT_PATH),size)


def render(phase=0, scale=1):
    from PIL import Image,ImageDraw
    im=Image.new('RGB',(990*scale,352*scale),INK)
    draw=ImageDraw.Draw(im)
    for points,fill in geometry(phase):
        draw.polygon([(round(x*scale),round(y*scale)) for x,y in points],fill=fill)
    draw.text((45*scale,27*scale),'NATIVE CODEX WORKFLOW',font=font(12*scale),fill=MUTED)
    draw.text((45*scale,256*scale),'THREE SESSIONS. ONE CONTRACT.',font=font(19*scale),fill=WHITE)
    for x,label in ((45,'THINKER'),(181,'DOER'),(305,'REVIEWER')):
        draw.text((x*scale,305*scale),label,font=font(11*scale),fill=MUTED)
    draw.text((694*scale,29*scale),'RESEARCH / BUILD / REVIEW',font=font(10*scale),fill=MUTED)
    for left,right in ((108,163),(222,287)):
        draw.line((left*scale,313*scale,right*scale,313*scale),fill=VIOLET,width=2*scale)
    return im


def workflow_base(phase=0):
    """A literal conceptual diagram; no session UI, telemetry or success state."""
    from PIL import Image,ImageDraw
    im=Image.new('RGB',(990,240),INK);d=ImageDraw.Draw(im)
    d.text((44,22),'RESEARCH. BUILD. REVIEW. THEN YOUR CALL.',font=font(17),fill=WHITE)
    roles=[('THINKER','Research',GREEN),('DOER','Build',WHITE),
           ('REVIEWER','Review',PINK),('YOU','Decide',GREEN)]
    for i,(name,action,color) in enumerate(roles):
        x=44+i*239
        d.polygon([(x,80),(x+12,80),(x,92)],fill=color)
        d.text((x,99),name,font=font(22),fill=WHITE)
        d.text((x,134),action,font=font(14),fill=MUTED)
        if i<3:
            d.line((x+139,113,x+207,113),fill=VIOLET,width=2)
            d.polygon([(x+207,109),(x+216,113),(x+207,117)],fill=VIOLET)
        offset=round(6*pulse(phase))
        d.polygon([(x+offset,173),(x+89+offset,173),
                   (x+83+offset,177),(x-6+offset,177)],fill=color)
    d.text((44,210),'WORKFLOW ILLUSTRATION / NO LIVE STATUS',font=font(11),fill=MUTED)
    return im


def workflow_frame(phase=0):
    return workflow_base(phase)


def workflow_svg():
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="990" height="240" viewBox="0 0 990 240" role="img" aria-labelledby="title desc">',
           '<title id="title">Research. Build. Review. Then your call.</title>',
           '<desc id="desc">Conceptual workflow illustration: Thinker researches, Doer builds, Reviewer reviews, and the human decides. Not a recording or live status.</desc>',
           '<rect width="990" height="240" fill="'+INK+'"/>',
           '<g font-family="monospace"><text x="44" y="38" font-size="17" fill="'+WHITE+'">RESEARCH. BUILD. REVIEW. THEN YOUR CALL.</text>']
    for i,(name,action,color) in enumerate([('THINKER','Research',GREEN),('DOER','Build',WHITE),('REVIEWER','Review',PINK),('YOU','Decide',GREEN)]):
        x=44+i*239
        parts.append(f'<path d="M{x} 80h12l-12 12z" fill="{color}"/>')
        parts.append(f'<text x="{x}" y="120" font-size="22" fill="{WHITE}">{name}</text>')
        parts.append(f'<text x="{x}" y="148" font-size="14" fill="{MUTED}">{action}</text>')
        parts.append(f'<path d="M{x} 173h89l-6 4h-89z" fill="{color}"/>')
        if i<3:parts.append(f'<path d="M{x+139} 113h68m0-4 9 4-9 4" fill="none" stroke="{VIOLET}" stroke-width="2"/>')
    parts.extend(['<text x="44" y="222" font-size="11" fill="'+MUTED+'">WORKFLOW ILLUSTRATION / NO LIVE STATUS</text></g>','</svg>'])
    return '\n'.join(parts)+'\n'


def main():
    global FONT_PATH
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parents[1]/'showcase/capri')
    parser.add_argument('--font',type=Path,required=True,help='Exact local Noto Sans Mono TTF; recorded by hash, never bundled')
    args=parser.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
    from PIL import Image,ImageDraw,ImageFont,__version__ as pillow_version
    chosen=ImageFont.truetype(str(args.font) if args.font else 'NotoSansMono-Regular.ttf',12)
    FONT_PATH=Path(chosen.path)
    (out/'capri-hero.svg').write_text(svg())
    render(scale=2).resize((990,352),Image.Resampling.LANCZOS).save(out/'capri-hero-static.png',optimize=True)
    frames=[]
    for i in range(90):
        frames.append(render(i/90,scale=2).resize((990,352),Image.Resampling.LANCZOS).quantize(colors=24,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE))
    frames[0].save(out/'capri-hero-loop.gif',save_all=True,append_images=frames[1:],
                   duration=[60,70,70]*30,loop=0,optimize=True,disposal=1)
    # Static social art: same composition, no animation dependency or external imagery.
    social=Image.new('RGB',(1280,640),INK)
    source=render(scale=2).resize((1188,422),Image.Resampling.LANCZOS)
    social.paste(source,(46,85));social.save(out/'capri-social-1280x640.png',optimize=True)
    # Small animated separators use the same palette and original abstract linework.
    divider=[]
    for i in range(45):
        im=Image.new('RGB',(990,24),INK);d=ImageDraw.Draw(im)
        for j in range(3):
            x=180+j*300+int(9*pulse(i/45))
            d.polygon([(x,10),(x+105,10),(x+97,14),(x-8,14)],fill=(GREEN,PINK,VIOLET)[j])
        divider.append(im.quantize(colors=8,dither=Image.Dither.NONE))
    divider[0].save(out/'capri-divider-loop.gif',save_all=True,append_images=divider[1:],
                    duration=[60,70,70]*15,loop=0,optimize=True,disposal=1)
    divider[0].convert('RGB').save(out/'capri-divider-static.png',optimize=True)
    (out/'workflow.svg').write_text(workflow_svg())
    workflow_frame().save(out/'workflow-static.png',optimize=True)
    flow=[workflow_frame(i/90).quantize(colors=24,method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.NONE) for i in range(90)]
    flow[0].save(out/'workflow-loop.gif',save_all=True,append_images=flow[1:],
                duration=[60,70,70]*30,loop=0,optimize=True,disposal=1)
    records=[]
    for p in sorted(out.iterdir()):
        if p.suffix in ('.png','.gif','.svg'):
            records.append(dict(path=p.name,bytes=p.stat().st_size,
                sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                source='ORIGINAL_CODE_AUTHORED_GEOMETRY_NO_THIRD_PARTY_CHARACTER_ART',
                status='AUTHORED_PRESENTATION_HUMAN_VISUAL_REVIEW_PENDING'))
    (out/'BUILD.json').write_text(json.dumps(dict(assets=records,model_image_generation=False,
        external_media_inputs=[],pillow_version=pillow_version,
        footer_font='System Noto Sans Mono; font software not bundled',
        font_sha256=hashlib.sha256(FONT_PATH.read_bytes()).hexdigest(),
        reproducibility='Same script, Pillow version and font bytes; SVG text also depends on viewer monospace font',
        source_frame_delays_ms=[60,70,70],human_continuous_motion_review='PENDING'),indent=2)+'\n')
    print(json.dumps(records,indent=2))


if __name__=='__main__':main()
