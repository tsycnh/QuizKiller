import cv2

if __name__ == '__main__':
    img = cv2.imread('test_images/冲顶0.jpg')
    cv2.imshow('img',img)
    answer = cv2.imread('冲顶answer_android.jpg')

    answer_h, answer_w, _ = answer.shape
    img_h, img_w, _ = img.shape
    r2 = cv2.matchTemplate(img, answer, method=cv2.TM_SQDIFF)
    answer_pos = cv2.minMaxLoc(r2)[2]  # (540,70)=>(x,y)
    # print(img_w,img_h)# 720 1280
    x_a = answer_pos[0]
    y_a = answer_pos[1]
    print('x_a',x_a,'y_a',y_a)
    x1,x2,y1,y2 = x_a,x_a+100,y_a,y_a+100
    vis = img.copy()[y1:y2, x1:x2]  ## img[top: bottom, left: right]
    ratio_x1,ratio_x2,ratio_y1,ratio_y2 = 0,0,0,0
    all_ratio = {
        'x1':ratio_x1,
        'x2':ratio_x2,
        'y1':ratio_y1,
        'y2':ratio_y2
    }

    def update_x1(ratio):
        ratio *= 0.001
        all_ratio['x1'] = round(ratio,3)
        global x1
        x1 = int(x_a + img_w * (ratio))
        if x1>=x2:
            x1 = x2-1
        print('x1:',x1,'x2:',x2,'y1:',y1,'y2:',y2)
        vis = img.copy()[y1:y2,x1:x2]## img[top: bottom, left: right]
        cv2.imshow('answer1', vis)
    def update_x2(ratio):
        ratio *= 0.001
        all_ratio['x2'] = round(ratio,3)
        global x2
        x2 = int(x_a + img_w * (ratio))
        if x2<=x1:
            x2=x1+1
        print('x1:',x1,'x2:',x2,'y1:',y1,'y2:',y2)
        vis = img.copy()[y1:y2,x1:x2]## img[top: bottom, left: right]
        cv2.imshow('answer1', vis)
    def update_y1(ratio):
        ratio *= 0.001
        all_ratio['y1'] = round(ratio,3)
        global y1
        y1 = int(y_a + img_h * (ratio))
        if y1>=y2:
            y1 = y2-1
        vis = img.copy()[y1:y2,x1:x2]## img[top: bottom, left: right]
        cv2.imshow('answer1', vis)
    def update_y2(ratio):
        ratio *= 0.001
        all_ratio['y2'] = round(ratio,3)
        global y2
        y2 = int(y_a + img_h * (ratio))
        if y2<=y1:
            y2 = y1+1
        vis = img.copy()[y1:y2,x1:x2]## img[top: bottom, left: right]
        cv2.imshow('answer1', vis)
    cv2.namedWindow('answer1',flags=cv2.WINDOW_NORMAL)
    cv2.imshow('answer1',vis)

    cv2.createTrackbar( "answer_x1", "answer1", 0, 1000, update_x1 )
    cv2.createTrackbar( "answer_x2", "answer1", 0, 1000, update_x2 )
    cv2.createTrackbar( "answer_y1", "answer1", 0, 1000, update_y1 )
    cv2.createTrackbar( "answer_y2", "answer1", 0, 1000, update_y2 )
    cv2.waitKey()
    cv2.destroyAllWindows()
    print(all_ratio)