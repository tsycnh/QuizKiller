import PIL
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
from PIL import ImageColor
from PIL import ImageFilter
import shutil
import os


def cvtImage(stext,fontFile,color_rgb):
    blank = Image.new("RGB", [32, 32],color_rgb)
    # drawObject = ImageDraw.Draw(blank)
    # Font1 = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SIMYOU.TTF",16)
    # drawObject.text([2,2],stext,font=Font1)
    # blank.show(title='1')
    image1 = add_text(blank,stext,fontFile)
    #image1.show()
    return image1
def add_text(image,text,font_file):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_file,size=30)
    txt = text
    font_size = font.getsize(text=txt)
    font_offset = font.getoffset(text=txt)
    # print(font_size,font_offset)
    if font_file == "msyh.ttc" or font_file == "msyhbd.ttc" or font_file == 'STXIHEI.TTF':
        offset_y = 3
    else:
        offset_y = 0
    t_x = int((image.width - font_size[0])/2)
    t_y = int((image.height - font_size[1])/2-offset_y)
    draw.text(xy=(t_x,t_y),text=txt,fill=(0),font=font)
    return image

def gaussBlur(image,radius):
    image = image.filter(ImageFilter.GaussianBlur(radius=radius))
    return image

def createImage():
    with open('source.txt','r') as fid:
        index = 0
        fontlist = ['Deng.ttf','msyh.ttc','STXIHEI.TTF','simhei.ttf','simkai.ttf','msyhbd.ttc','simsun.ttc','simyou.ttf']
        colorList = ["#FFFFFF","#E6E6E6","#c8c8c8"]
        blurRadiusList=[0,0.6,1,1.3]
        os.mkdir('images32/')
        while True:
            stext = fid.readline()
            if stext=='':
                break
            stext = stext.strip('\n')
            print(stext)
            dir_name = "%04d" % index
            os.mkdir('images32/' + dir_name)
            fname = 0
            for ft in fontlist:
                for cl in colorList:
                    for br in blurRadiusList:
                        imPath='images32/'+ dir_name+'/'+str(fname)+'.jpg'
                        image = cvtImage(stext,fontFile='fonts/'+ft,color_rgb=cl)
                        image = gaussBlur(image,br)
                        image.save(imPath)
                        fname = fname+1;
            index = index+1

def test():
    im = cvtImage("艘",'Deng.ttf',"#e6e6e6")
    im2 = gaussBlur(im,0.6)
    im.show()
    im2.show()






if __name__ == "__main__":
    createImage()