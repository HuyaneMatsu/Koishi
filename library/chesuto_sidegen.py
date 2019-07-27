from PIL import Image as PIL
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import truetype

class ms_cache(object):
    __slots__=['parent', 'obj']

    def get_doc(self):
        return self.parent.klass.__doc__
    def set_doc(self,value):
        self.parent.klass.__doc__=value
    __doc__=property(get_doc,set_doc)
    del get_doc,set_doc

    def __init__(self,parent,obj):
        self.parent=parent
        self.obj=obj
        
    def __call__(self,*args,**kwargs):
        return self.parent.klass(self.obj,*args,**kwargs)
    
class methodsimulator(object):
    __slots__=['klass']
    
    def get_doc(self):
        return self.klass.__doc__
    def set_doc(self,value):
        self.klass.__doc__==value
    __doc__=property(get_doc,set_doc)
    del get_doc,set_doc
   
    def __init__(self,klass):
        self.klass=klass
        
    def __get__(self,obj,objtype=None):
        if obj is None:
            return self.klass
        return ms_cache(self,obj)

    def __set__(self,obj,value):
        raise AttributeError('can\'t set attribute')
    def __delete__(self,obj):
        raise AttributeError('can\'t delete attribute')

PIL.Image.draw=methodsimulator(ImageDraw)
PIL.font=truetype
del ImageDraw,truetype

def char_range(start,end):
    for x in range(ord(start),ord(end)+1):
        yield chr(x)


FONT=PIL.font('Kozuka.otf',50)
FONT_COLOR=(0,0,0)

size=53

DC=(181,136,99)
BC=(240,217,181)

side_size=8
   
for text in char_range('1','8'):
    image=PIL.new('RGB',(size,size),BC)
    image.draw().rectangle((0,0,side_size,53),fill=DC)
    text_size=FONT.getsize(text)
    image.draw().text((side_size+((size-side_size-text_size[0])>>1),((size-text_size[1])>>1),),text,fill=FONT_COLOR,font=FONT)
    image.save(f'CHESUTO_S{text}.png')

image=image=PIL.new('RGB',(size,size),BC)
image.draw().rectangle((0,0,side_size,53),fill=DC)
image.draw().rectangle((side_size,0,53,side_size),fill=DC)
image.save(f'CHESUTO_SX.png')

for text in char_range('A','H'):
    image=PIL.new('RGB',(size,size),BC)
    image.draw().rectangle((0,0,53,side_size),fill=DC)
    text_size=FONT.getsize(text)
    image.draw().text((((size-text_size[0])>>1),side_size+((size-side_size-text_size[1])>>1),),text,fill=FONT_COLOR,font=FONT)
    image.save(f'CHESUTO_S{text}.png')
