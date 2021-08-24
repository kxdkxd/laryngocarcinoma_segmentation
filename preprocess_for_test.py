import cv2
import random
import numpy as np
import nibabel as nib

def split_imgs(img_path):
    img = nib.load(img_path)
    img = img.get_data()
    imgs = np.split(img, img.shape[2], axis=2)
    return imgs

data_list = []

for file_id in range(1, 1+1):  # file id
    src_path = 'dataset/TestSet/%03d.nii.gz' % file_id
    src_imgs = split_imgs(src_path)
    for src, index in zip(src_imgs, range(len(src_imgs))):
        src = ((src-np.min(src))/(np.max(src)-np.min(src))*255).astype('uint8')
        cv2.imwrite('dataset/srcs/%02d_%04d.jpg' % (file_id, index), src)
        data_list.append('srcs/%02d_%04d.jpg labels/%02d_%04d.jpg\n' % (file_id, index, file_id, index))

# random.shuffle(data_list)

# with open('dataset/train.txt', 'w') as f:
#     for line in data_list[:-50]:
#         f.write(line)

with open('dataset/test.txt', 'w') as f:
    for line in data_list:
        f.write(line)