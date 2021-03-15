from PIL import Image
import sys
import os

from math import log

name=os.path.join(os.path.abspath('.'),sys.argv[1])

ori=Image.open(name)
new=ori.convert('RGBA')
to_clear=(0,0,0)

zero=tuple(0 for a in range(4))

pixels=new.load()

for x in range(ori.width):
    for y in range(ori.height):
        r,g,b,a=pixels[x,y]
        if (r,g,b)==to_clear:
            pixels[x,y]=zero
                    
new.save(name)
