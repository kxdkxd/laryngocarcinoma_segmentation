# laryngocarcinoma_segmentation
 Laryngocarcinoma Segmentation on CT Nii files, with OCRNet on 2D z-axis slices, implemented and tested on Python3 and Paddle 2.0.2

 *Note: Paddle framework is much as similar as  PyTorch.*

# Before Run
## Basic System Environment
### Hardware
**For Training**

- Tested on Baidu AIStudio, with NVIDIA Tesla V100 - 32GiB VideoMem. While training, around 24GiB VideoMem will be used with batch_size is set to 12. Lower the batch_size can significantly reduce the VideoMem cost, but as an important hyper-parameter, this move can lead to different performance as I do.

- As a result, a GPU with large VideoMem is recommended.

**For Testing**

- Tested on Baidu AIStudio, with pure CPU, really slow and ended up with Error. However works great with a GPU.

- A Normal GPU can handle testing job.


### Software

- Python 3 (Tested on Python 3.7)
- Paddle 2.0.2
- paddleseg (Tested on pip installed paddleseg 2.2.0)
- nibabel (Tested on pip installed nibabel 3.2.1)
- ITK-SNAP (3.6.0) (For 3D nii data visualization)


## Tutorial

### **Install packages:**

``pip install nibabel paddleseg``


### **Download OCRNet pre-train model:**

``wget https://bj.bcebos.com/paddleseg/dygraph/cityscapes/ocrnet_hrnetw48_cityscapes_1024x512_160k/model.pdparams -o model_pretained_bcebos.pdparams``


### **Construct Directories:**
```bash
mkdir dataset
mkdir dataset/srcs
mkdir dataset/labels
mkdir dataset/labels_show
mkdir outputs
```

### **Download dataset:**

Download from BaiduNetdisk, place TrainSet.zip TrainLabel.zip to dataset directory. Place outputs.zip to the project root directory if you just want to perform test job.
```
https://pan.baidu.com/s/1NZ0UyAq5c_dno-N1pojSVA  code: kkkk
```
``unzip outputs.zip``

``cd dataset/ && unzip TrainSet.zip && unzip TrainLabel.zip``

*Note: The dataset-08 is mal-formed. The label should be {0, 1} while {2} occured, and the volume of labeled data is abnomarlly laege. Pay attention to this one.*

The given best model can achieve mIoU: 0.8355 Acc: 0.9991 Kappa: 0.8040 ,Class IoU: [0.9991 0.6719], Class Acc: [0.9996 0.7973] on given dataset.


**For Training and Validating**
### **Preprocess dataset:**
``python preprocess_for_train.py``

dataset divided train/val = 9/1. You can Edit this line.
```python
test_data_size = int(len(data_list) * 0.1)
```
**Train**

``python train.py --config OCRNet_W48.yml --do_eval --save_interval 50 --save_dir outputs``

**Validate**

``python val.py --config OCRNet_W48.yml --model_path outputs/best_model/model.pdparams`` 

**For Testing**
### **Preprocess dataset:**
``python preprocess_for_test.py``

``python predict.py --config OCRNet_W48.yml --model_path output/best_model/model.pdparams --image_path dataset/srcs --save_dir results``