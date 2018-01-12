from PIL import ImageGrab


#addr = 'D:/TensorflowDoc/screen_grab/a.jpg'


def getScreenROI(box):
    im = ImageGrab.grab()
    # im.save(addr)

    #box = (100, 100, 500, 500)
    region = im.crop(box)
    #region.show()
    return region



#