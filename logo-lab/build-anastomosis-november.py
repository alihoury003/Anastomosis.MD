#!/usr/bin/env python3
"""Rebuild the 70-mark Anastomosis November shortlist from repository root.

Requires Pillow and NumPy. If rapidocr-onnxruntime is installed, OCR checks
are run against the actual shortlist header; absence of OCR is reported.
"""
import os
from pathlib import Path
os.chdir(Path(__file__).resolve().parent.parent)
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import numpy as np
try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError:
    RapidOCR = None
paths=sorted(Path('logo-lab').glob('fresh-[0-9][0-9]-*.png'))+sorted(Path('logo-lab').glob('november-[0-9][0-9]-*.png'))
assert len(paths)==70, f"Expected 70 marks, found {len(paths)}"
for i, path in enumerate(paths, start=1):
    actual = int(path.name.split('-')[1])
    assert actual == i, f"Expected {i:02d}, found {path.name}"
BG=(247,243,235); INK=(16,20,24); PETROL=(27,78,95); RED=(181,52,42); RULE=(227,220,204)
W,H=2400,10300; img=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(img)
serif=ImageFont.truetype('social-kit/fonts/InstrumentSerif-Italic.ttf',108)
mono=ImageFont.truetype('social-kit/fonts/JetBrainsMono-Regular.ttf',25)
small=ImageFont.truetype('social-kit/fonts/JetBrainsMono-Regular.ttf',20)
d.text((100,55),'Anastomosis November',font=serif,fill=INK)
d.text((105,190),'70 CIRCLE PREVIEWS  /  61—70 NEW  /  V7',font=mono,fill=PETROL)
d.line((100,255,2300,255),fill=RULE,width=3)
start_x=100; gap_x=25; cell_w=531; row_h=552; y0=290; size=465
for i,p in enumerate(paths):
 c=i%4;r=i//4;x=start_x+c*(cell_w+gap_x);y=y0+r*row_h
 logo=Image.open(p).convert('RGB').resize((size,size),Image.Resampling.LANCZOS)
 # Simulate the actual Instagram circle crop, not just an outline on a square.
 circular_mask=Image.new('L',(size,size),0)
 ImageDraw.Draw(circular_mask).ellipse((0,0,size-1,size-1),fill=255)
 avatar=Image.new('RGB',(size,size),BG)
 avatar.paste(logo,(0,0),circular_mask)
 icon_x=x+(cell_w-size)//2
 img.paste(avatar,(icon_x,y))
 d.ellipse((icon_x,y,icon_x+size-1,y+size-1),outline=RULE,width=2)
 d.line((x,y+477,x+cell_w,y+477),fill=RULE,width=2)
 d.text((x+3,y+493),f'{i+1:02d}',font=mono,fill=RED if i<10 else PETROL)
 d.text((x+cell_w,y+495),'CIRCLE',font=small,fill=(128,126,117),anchor='ra')
img.save('logo-lab/anastomosis-november.png',optimize=True)
print('saved',img.size,'with',len(paths),'symbols')
# Read exactly what the final raster actually contains; no synthetic proof.
if RapidOCR is not None:
    head=img.crop((50,20,2300,260));res,_=RapidOCR()(np.asarray(head))
    print('actual header OCR:',[(x[1],round(float(x[2]),3)) for x in (res or [])])
    joined=' '.join(x[1] for x in (res or [])).lower()
    if 'anastomosis' not in joined or 'november' not in joined:raise SystemExit('TITLE OCR FAILED')
    print('title OCR PASS')
else:
    print('OCR unavailable — verify the title before showing this file')
