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

for file_id in [_ for _ in range(1, 7+1)] + [_ for _ in range(9, 90+1)]: # File ID, from 001-007, 009- 090
	src_path = 'dataset/TrainSet/%03d.nii.gz' % file_id
	label_path = 'dataset/TrainLabel/%03d.nii.gz' % file_id
	src_imgs = split_imgs(src_path)
	label_imgs = split_imgs(label_path)
	dataset = list(zip(src_imgs, label_imgs, range(len(src_imgs))))
	for src, label, index in dataset:
		src = ((src-np.min(src)) / (np.max(src)-np.min(src))*255).astype('uint8')
		if np.sum(label>0) == 0:
			continue
		if np.sum(label==2) > 0:
			continue
		cv2.imwrite('dataset/srcs/%02d_%04d.jpg' % (file_id, index), src)
		cv2.imwrite('dataset/labels/%02d_%04d.jpg' % (file_id, index), label)
		cv2.imwrite('dataset/labels_show/%02d_%04d.jpg' % (file_id, index), label*255)
		data_list.append('srcs/%02d_%04d.jpg labels/%02d_%04d.jpg\n' % (file_id, index, file_id, index))


random.shuffle(data_list)
print("len_data=")
print(len(data_list))
test_data_size = int(len(data_list) * 0.1)

with open('dataset/train.txt', 'w') as f:
	for line in data_list[test_data_size:]:
		f.write(line)

with open('dataset/val.txt', 'w') as f:
	for line in data_list[:test_data_size]:
		f.write(line)