import shutil
import random
import os
# 将数据集打乱并分成训练集和测试集
random.seed(0)
root_dir = './images32/'
target_dir = './chnData/'
target_train_dir = target_dir+'train/'
target_test_dir = target_dir+'test/'
if os.path.exists(target_dir):
    shutil.rmtree(target_dir)
os.makedirs(target_dir)
dirs = os.listdir(root_dir)

for dir in dirs:
    f_dir = os.path.join(root_dir,dir)
    img_names = []
    for _,_,file in os.walk(f_dir):
        img_paths = []
        d_train_dir = f_dir.replace(root_dir,target_train_dir)
        d_test_dir = f_dir.replace(root_dir,target_test_dir)
        os.makedirs(d_train_dir)
        os.makedirs(d_test_dir)
        for f in file:
            img_paths.append(os.path.join(f_dir,f))
        random.shuffle(img_paths)

        for i in range(0,6):
            target_path = img_paths[i].replace(root_dir,target_train_dir)
            shutil.copy(img_paths[i],target_path)

        for i in range(6,8):
            target_path = img_paths[i].replace(root_dir,target_test_dir)
            shutil.copy(img_paths[i],target_path)
        print(f_dir,'copied')
    # shutil.copy()