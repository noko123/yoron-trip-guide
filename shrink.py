import os
from PIL import Image, ImageOps
os.makedirs('use',exist_ok=True)
tot=0
for f in sorted(os.listdir('use')):
    p=os.path.join('use',f)
    im=Image.open(p); im=ImageOps.exif_transpose(im).convert('RGB')
    maxw=1000
    if im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    im.save(p,'JPEG',quality=74,optimize=True,progressive=True)
    tot+=os.path.getsize(p)
    print(f, im.size, os.path.getsize(p)//1024,'KB')
print('total %.2f MB'%(tot/1e6))
