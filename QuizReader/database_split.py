import shutil
import random
import os
# 将数据集打乱并分成训练集和测试集
random.seed(0)
root_dir = './images32/'
target_dir = './chnData/'
train_ratio = 0.8
test_ratio = 1-train_ratio
max_folder_digits_count = 4# 单个类别图片所在文件夹名称最长位数。比如0023,就是4。02399就是5
# =========
target_train_dir = target_dir+'train/'
target_test_dir = target_dir+'test/'
if os.path.exists(target_dir):
    shutil.rmtree(target_dir)
os.makedirs(target_dir)
dirs = os.listdir(root_dir)
def extend_name(origin):
    l = len(origin)
    output = ''
    for i in range(max_folder_digits_count-l):# 一共4位
        output +='0'
    output += origin
    return output
for dir in dirs:
    f_dir = os.path.join(root_dir,dir)
    index = f_dir.rfind('/')
    pre = f_dir[:index+1]
    num = f_dir[index+1:]
    new_f_dir = pre+ extend_name(num)
    img_names = []
    for _,_,file in os.walk(f_dir):
        img_paths = []
        d_img_paths = []
        d_train_dir = new_f_dir.replace(root_dir,target_train_dir)
        d_test_dir = new_f_dir.replace(root_dir,target_test_dir)
        os.makedirs(d_train_dir)
        os.makedirs(d_test_dir)
        for f in file:
            img_paths.append(os.path.join(f_dir,f))
            d_img_paths.append(os.path.join(new_f_dir,f))
        random.shuffle(img_paths)

        imgs_count = len(file)
        split = int(train_ratio*imgs_count)
        for i in range(0,split):
            target_path = d_img_paths[i].replace(root_dir,target_train_dir)
            shutil.copy(img_paths[i],target_path)

        for i in range(split,imgs_count):
            target_path = d_img_paths[i].replace(root_dir,target_test_dir)
            shutil.copy(img_paths[i],target_path)
        print(f_dir,'copied')
    # shutil.copy()