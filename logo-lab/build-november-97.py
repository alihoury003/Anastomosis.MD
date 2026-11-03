#!/usr/bin/env python3
"""Rebuild concept 97 with flat red and petrol vector-style shapes.
Run: python logo-lab/build-november-97.py (requires Pillow).
"""
from pathlib import Path
from PIL import Image, ImageDraw
S=3;im=Image.new('RGB',(1024*S,1024*S),(247,243,235));d=ImageDraw.Draw(im)
def render(start,segments,fill):
 pts=[start];p=start
 for typ,coords in segments:
  if typ=='L':p=coords;pts.append(p)
  if typ=='C':
   a,b,c=coords
   for i in range(1,33):
    t=i/32;u=1-t;pts.append((u**3*p[0]+3*u*u*t*a[0]+3*u*t*t*b[0]+t**3*c[0],u**3*p[1]+3*u*u*t*a[1]+3*u*t*t*b[1]+t**3*c[1]))
   p=c
 d.polygon([(round(x*S),round(y*S)) for x,y in pts],fill=fill)
red=(181,52,42);blue=(27,78,95)
render((215,340),[('C',((215,295),(250,260),(295,260))),('L',(605,260)),('C',((644,260),(672,286),(672,324))),('C',((672,359),(645,385),(608,385))),('L',(373,385)),('C',((351,385),(338,400),(338,423))),('L',(338,505)),('C',((338,533),(315,555),(285,555))),('L',(267,555)),('C',((237,555),(215,533),(215,505)))],red)
render((809,684),[('C',((809,729),(774,764),(729,764))),('L',(419,764)),('C',((380,764),(352,738),(352,700))),('C',((352,665),(379,639),(416,639))),('L',(651,639)),('C',((673,639),(686,624),(686,601))),('L',(686,519)),('C',((686,491),(709,469),(739,469))),('L',(757,469)),('C',((787,469),(809,491),(809,519)))],blue)
render((300,476),[('C',((386,465),(450,447),(512,448))),('L',(512,520)),('C',((450,520),(386,540),(300,545)))],red)
render((512,448),[('C',((574,448),(638,478),(706,493))),('L',(706,567)),('C',((638,552),(574,520),(512,520)))],blue)
im.resize((1024,1024),Image.Resampling.LANCZOS).save(Path(__file__).resolve().with_name('november-97-flow.png'))
