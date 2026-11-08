from html.parser import HTMLParser
import subprocess
from pathlib import Path
class Capture(HTMLParser):
 def __init__(self,src):
  super().__init__(convert_charrefs=False);self.src=src;self.lines=src.splitlines(keepends=True);self.offsets=[];n=0
  for l in self.lines:self.offsets.append(n);n+=len(l)
  self.stack=[];self.captured={};self.styles=[]
 def off(self):
  line,col=self.getpos();return self.offsets[line-1]+col
 def handle_starttag(self,tag,attrs):
  start=self.off();fields=dict(attrs);target=fields.get('id');isstyle=tag=='style'
  if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append((tag,start,target,isstyle))
 def handle_startendtag(self,tag,attrs):pass
 def handle_endtag(self,tag):
  for idx in range(len(self.stack)-1,-1,-1):
   if self.stack[idx][0]==tag:
    popped=self.stack[idx:];self.stack=self.stack[:idx];end=self.src.find('>',self.off())+1
    for t,start,target,isstyle in popped:
     if target in {'screen-block','endModal','issueModal','labPanel','labPopup'}:self.captured.setdefault(target,[]).append(self.src[start:end])
     if isstyle:self.styles.append(self.src[start:end])
    break
 def finish(self):self.feed(self.src);self.close();return self.captured,self.styles
base=subprocess.check_output(['git','show','2d8d0d0:dashboard.html']).decode();stage=Path('payment-integration/dashboard.html').read_text()
a,sa=Capture(base).finish();b,sb=Capture(stage).finish()
for key in ('screen-block','endModal','issueModal','labPanel','labPopup'):
 assert a.get(key)==b.get(key),f'Protected markup changed: {key}'
 print(key,'preserved' if key in a else 'absent from both')
assert sa==sb,'Styles changed';print('all stylesheet blocks preserved')
