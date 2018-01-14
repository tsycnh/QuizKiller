import cv2
# 判断两矩形是否相交，若相交返回相交面积，否则返回-1,gap表示两个矩形之间如果有gap大小的距离也算相交
def rect_interaction(rect1,rect2,gap = 0):
    #rect1 = [x1,y1,x2,y2]  x1,y1 左上角矩形坐标 x2,y2 右下角矩形坐标
    x1,y1,x2,y2 = rect1[0]-gap,rect1[1]-gap,rect1[2]+gap,rect1[3]+gap
    x3,y3,x4,y4 = rect2[0]-gap,rect2[1]-gap,rect2[2]+gap,rect2[3]+gap

    a = max(x1,x3)
    b = min(x2,x4)
    c = max(y1,y3)
    d = min(y2,y4)

    if (a-b<=0 and c-d<=0):
        return (b-a)*(d-c)
    else:
        return -1

# 合并两个矩形
def merge_rects(rect1,rect2):
    #rect1 = [x1,y1,x2,y2]
    x1, y1, x2, y2 = rect1[0], rect1[1], rect1[2], rect1[3]
    x3, y3, x4, y4 = rect2[0], rect2[1], rect2[2], rect2[3]

    new_rect = [min(x1,x3),min(y1,y3),max(x2,x4),max(y2,y4)]
    return new_rect

def merge_group_rects(rects,gap=0):
    while True:
        found_interaction = False
        for i in range(len(rects) - 1):
            for j in range(i + 1, len(rects)):
                r1 = rects[i]
                r2 = rects[j]
                if rect_interaction(r1, r2, gap=gap) > 0:  # 若相交
                    # print('发现相交')
                    new_r = merge_rects(r1, r2)
                    del rects[j]
                    del rects[i]
                    rects.append(new_r)
                    found_interaction = True
                    break
        # print('====')
        if not found_interaction:
            break
    # return rects

# 矩形坐标转换
def coordinate_transfer(rect):
    # rect = [x,y,w,h] =》[x,y,x+w,y+h]
    return [rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3]]

# 删除周长过小的矩形
def reduce_rects(rects,thresh_area):
    for i in range(len(rects)-1,-1,-1):
        rect = rects[i]
        round = ((rect[2]-rect[0])+(rect[3]-rect[1]))*2
        # print('i:',i,'area:',area)
        if round<=thresh_area:
            del rects[i]
            # print('该删')
    return rects

# 在图像中绘制矩形们
def draw_rects(image,rects):
    image = image.copy()
    for i,rs in enumerate(rects):
        cv2.rectangle(image, (int(rs[0]), int(rs[1])), (int(rs[2]), int(rs[3])), (0))
        cv2.putText(image,text=str(i),org=(rs[0],rs[1]),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.5,color=(0))
    return image

# 按照new_long大小来
def image_resize(image,new_long):
    h = image.shape[0]
    w = image.shape[1]
    if w >= h:
        new_w = new_long
        new_h = (new_w*h)/w
    else:
        new_h = new_long
        new_w = (new_h*w)/h

    return cv2.resize(image,(int(new_w),int(new_h)))

def find_first_greater_value(value,list):
    for i,v in enumerate(list):
        if v>=value:
            return i
    return -1