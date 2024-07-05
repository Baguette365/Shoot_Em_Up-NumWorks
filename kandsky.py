from kandinsky import get_pixel as gp,set_pixel as sp,fill_rect as fr,draw_string as ds,color
HEX=lambda v,l=2: ('%'+"0%sx"%l)%v
INT=lambda v: int("0x"+v,16)
get_hpixel=lambda x,y: "#%02x%02x%02x"%gp(x,y)
def draw_circle(x,y,radius,color,back=None,spader=1,semi=False,reverse=False):
 ra,s=radius,spader
 r,rr,s=ra**2,ra*2,(s+9)**2 if s>0 else 0
 for i in range(r<<(1 if semi else 2)):
  tx,ty=(i%rr)-ra,(i//rr)-ra
  if r+s<=tx**2+ty**2>=r if reverse else r+s>=tx**2+ty**2<=r:sp(x+tx,y+ty,color)
  elif back!=None:sp(x+tx,y+ty,back)
fill_circle=lambda x,y,radius,color,back=None,semi=False,reverse=False:draw_circle(x,y,radius,color,back,radius,semi,reverse)
def draw_rect(x,y,w,h,color,spader=1):
 c,s=color,spader
 fr(x,y,w,s,c)
 fr(x,y,s,h,c)
 fr(x+w,y,s,h,c)
 fr(x,y+h,w,s,c)
def draw_line(x1,y1,x2,y2,color,spader=1):
 c,ss=color,spader
 if ss<1:return
 s=abs(y2-y1)>abs(x2-x1)
 if s:x1,y1,x2,y2=y1,x1,y2,x2
 if x1>x2:x1,x2,y1,y2=x2,x1,y2,y1
 g=1 if x2==x1 else(y2-y1)/(x2-x1)
 for x in range(x1,x2):
  y2=int(y1+g*(x-x1))
  fr(y2,x,ss,ss,c)if s else fr(x,y2,ss,ss,c)
def get_screen(x,y,w,h,compress=False):
 if compress:
  pa,hh,c,o,w,h='','',0,0,w*2,h*2
  for i in range(w*h):
   p=get_hpixel(x+(i%w)-w,y+(i//h)-h)
   if p not in pa:pa+=p
  mpa,mh=pa.count('#')>>8+1,h>>8+1
  for i in range(w*h):
   ty=(i//h)-h
   p,c=pa.index(get_hpixel(x+(i%w)-w,y+ty))//7,c+1
   if o!=p or ty>=h:c,o,hh=0,p,hh+HEX(p,mpa)+HEX(c,mh)
  #     |--------------- HEADER ---------------||- COLORS PALLET -|| HASH |
  return HEX(w,3)+HEX(h,3)+HEX(pa.count('#'),6)+pa.replace('#','')+hh
 else: return [[get_hpixel(x+xx,y+yy)for yy in range(h)]for xx in range(w)]
def parse_screen(x,y,hash,zoom=1):
 hh,z=hash,zoom
 del hash
 if type(hh)==str:
  w,h,c=INT(hh[:3]),INT(hh[3:6]),INT(hh[6:12])
  c,hh,pa,hh,s,tx,ty=c>>8+1,h>>8+1,hh[12:c*6],hh[12+c*6:],0,0,0
  while hh!='':
   s,ty,i,hh=INT(hh[c:c+hh]),ty+s,INT(hh[:c])*6,hh[c+hh:]
   fr(x+tx,y+ty,z,s*z,'#'+pa[i:i+6])
   if ty>=h:tx,ty=tx+z,0
 else:[[sp(x+tx,y+ty,p)for ty,p in enumerate(l)]for tx,l in enumerate(hh)]
def draw_text(text,x,y,size=1,color_=(0,0,0),bg=(248,252,248),hideModel=True):
 s,l,c,hm,ss=10*len(text.replace('\t',"    ")),18*(text.count('\n')+1),color_,hideModel,size
 hc,hbg=c==None,bg==None
 if hc and hbg:return
 if hm: o=get_screen(0,0,s,l,True)
 ds(text,0,0,**({"color":c} if hc else {})+({"background":bg} if hbg else {}))
 e=color(c) if hc else color(bg) if hbg else False
 [[fr(x+xx*(ss+1)-xx,y+yy*(ss+1)-yy,ss,ss,gp(xx,yy)) for yy in range(l)if gp(xx,yy)!=e]for xx in range(s)]
 if hm:parse_screen(0,0,o)
