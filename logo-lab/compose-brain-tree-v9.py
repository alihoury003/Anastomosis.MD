#!/usr/bin/env python3
"""Build the V9 brain-tree concept from its generated text-free base.

Run from any directory: python logo-lab/compose-brain-tree-v9.py
Requires Pillow, NumPy and rapidocr-onnxruntime. OCR is performed on image
pixels extracted from each glyph and straightened, not on the full image.
The result is an approval concept; it is not wired into the website.
"""
import os
from pathlib import Path
from tempfile import gettempdir
os.chdir(Path(__file__).resolve().parent.parent)
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
import numpy as np
from rapidocr_onnxruntime import RapidOCR
BONE=(247,243,235); CRIMSON=(181,52,42); PETROL=(27,78,95)
word='anastomosis'; assert len(word)==11
im=Image.open('logo-lab/brain-tree-structure-v9.png').convert('RGB'); S=3
font=ImageFont.truetype('social-kit/fonts/InstrumentSerif-Italic.ttf',150*S)
adv=[font.getlength(c)/S for c in word]; spacing=7; total=sum(adv)+spacing*(len(word)-1); x=(1024-total)/2
masks=[]
for i,ch in enumerate(word):
 center=x+adv[i]/2
 # Follow a shallow crown arc, without rotating/distorting glyphs.
 baseline=205+47*((center-512)/400)**2
 full=Image.new('L',(1024*S,1024*S));d=ImageDraw.Draw(full)
 d.text((int(x*S),int(baseline*S)),ch,font=font,fill=255,anchor='ls',stroke_width=1*S)
 full=full.resize((1024,1024),Image.Resampling.LANCZOS).filter(ImageFilter.MinFilter(3));masks.append(full)
 x+=adv[i]+spacing
for i in range(10):
 a=np.asarray(masks[i])>128;b=np.asarray(masks[i+1])>128
 print('adjacent',i+1,i+2,int((a&b).sum()))
# thin separation from the vascular background without hard white blocks.
halo=Image.new('L',(1024,1024))
for m in masks:halo=ImageChops.lighter(halo,m.filter(ImageFilter.MaxFilter(9)))
halo=halo.filter(ImageFilter.GaussianBlur(1.4))
im=Image.composite(Image.new('RGB',im.size,BONE),im,halo)
# Fine vessel stems join the lower edge of each letter to the crown.
draw=ImageDraw.Draw(im)
for i,m in enumerate(masks):
 a=np.asarray(m); ys,xs=np.where(a>200)
 bottom=ys.max(); near=xs[ys>=bottom-4]
 if not len(near): continue
 x0=int(np.median(near)); y0=int(bottom-2)
 direction=-1 if i%2==0 else 1
 color=CRIMSON if i<4 else PETROL
 points=[(x0,y0),(x0+direction*3,y0+10),(x0+direction*9,y0+21),(x0+direction*14,y0+32)]
 for j in range(len(points)-1): draw.line([points[j],points[j+1]], fill=color,width=4-j)
 draw.line([(x0+direction*9,y0+21),(x0-direction*3,y0+30)],fill=color,width=2)
# Ink letters on same artery/vein colors as illustration.
for i,m in enumerate(masks): im=Image.composite(Image.new('RGB',im.size,CRIMSON if i<4 else PETROL),im,m)
im.save('logo-lab/brain-tree-v9.png')
# OCR verification: actual image pixels isolated by letter masks, unrolled to
# a common baseline. This does not replace judging the curved final image.
tiles=[]
for m in masks:
 b=m.getbbox(); crop=im.crop(b); mask=m.crop(b);tile=Image.new('RGB',crop.size,BONE);tile.paste(crop,(0,0),mask);tiles.append(tile)
# Normalized baseline and near-natural spacing, preserving real pixel glyphs.
for gap in (4,7,10):
 strip=Image.new('RGB',(sum(t.width for t in tiles)+gap*(len(tiles)+1),200),BONE); x=gap
 for t in tiles:strip.paste(t,(x,160-t.height));x+=t.width+gap
 res,_=RapidOCR()(np.asarray(strip));print('extracted image glyph OCR gap',gap,[r[1] for r in res] if res else [])
 strip.save(str(Path(gettempdir()) / ('brain-extracted-%d.png' % gap)))
