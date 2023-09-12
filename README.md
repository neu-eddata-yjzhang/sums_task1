## 任务一：航拍复杂图像目标检测说明

### 0. 环境部署

    # 创建虚拟环境
    conda create -n detect python=3.8
    # 激活虚拟环境
    conda activat detect

    # 安装依赖
    pip install -r requirements.txt

### 1. 数据准备 


- 在'dataset'文件夹下新建一个'data'目录并将Task1的数据按 9:1 划分用来测试模型效果

    将所有数据和'split.py'放在'data'目录下，格式为：
```
  ├── images:  原始数据，包含*.jpg 都在一个目录下
  ├── labels: 标注的数据类别
  └── split.py: 划分训练数据集
```
- 运行程序 'split.py', 得到如下结果

    python split.py

```
  ├── train:  训练集
    ├── imgnamefile.txt : 训练集的图片名
    ├── images: 训练用的图片
    └── labelTxt: 训练标签
  ├── val:  验证集
    ├── imgnamefile.txt : 验证集的图片名
    ├── images: 验证用的图片
    └── labelTxt: 验证标签
  ├── images:  原始数据，包含*.jpg 都在一个目录下
  ├── labels: 标注的数据类别
  └── split.py: 划分训练数据集
```

- 当用全部训练集的数据训练数据以提交测试模型在测试集上的效果时

    1. 在'dataset'文件夹下新建一个'full_data'目录,在'full_data'下新建'train'和'val'两目录,并分别在两目录下创建'images','labelTxt','imgnamefile.txt'。
    2. 将'dataset/data/train/images'和'dataset/data/val/images'中的全部图片复制到'dataset/full_data/train/images'
    3. 将'dataset/data/train/labelTxt'和'dataset/data/val/labelTxt'中的全部txt复制到'dataset/full_data/train/labelTxt'
    4. 将'dataset/data/train/imgnamefile.txt'和'dataset/data/val/imgnamefile.txt'中的全部内容合并并复制到'dataset/full_data/train/imgnamefile.txt'
    5. 从中任选一张图片按照如上过程配置'val'文件夹。
    ```
    ├── train:  包含训练集全部数据
        ├── imgnamefile.txt : 训练集的图片名
        ├── images: 训练用的图片
        └── labelTxt: 训练标签
    └──  val:  验证集仅保留一张出现在训练集中的图片即可，在用全部数据训练时不需要观察模型在验证集上的结果。
        ├── imgnamefile.txt : 验证集的图片名
        ├── images: 验证用的图片
        └── labelTxt: 验证标签
    ```

### 2. 训练/测试模型

######训练模型（单卡）
    nohup python -u train.py --device 5 > '日志名' 2>&1 & # nohup python -u train.py --device 5 > test.log 2>&1 & 

######训练模型（二卡, 6,7）
    nohup python -u -m torch.distributed.launch --nproc_per_node 2 train.py --device 6,7 > '日志名' 2>&1 &

######训练模型（四卡,1,2,3,4）
    nohup python -u -m torch.distributed.launch --nproc_per_node 4 train.py --device 1,2,3,4 > '日志名' 2>&1 &

######测试模型效果

    nohup python -u detect.py --weights '模型地址' \
    --source '测试集图片存放地址' \
    --img 2048 --device 4,5,6,7 --conf-thres 0.25 --iou-thres 0.2 --hide-labels --hide-conf > '日志名' 2>&1 & 

    exp:
    nohup python -u detect.py --weights '/home/work/zhangyijia/sjms/task1_code/runs/train/exp12/weights/best.pt' \
    --source '/home/work/zhangyijia/sjms/datasets/Task1_Test/images/' \
    --img 2048 --device 4,5,6,7 --conf-thres 0.25 --iou-thres 0.2 --hide-labels --hide-conf > log_fulldata/zyj_test_modelsizev7_0907.log 2>&1 & 

#####使用全训练集训练模型以提交计算测试集结果

    1. 修改'/home/work/zhangyijia/sjms/task1_code/data/DroneVehicle_poly.yaml'
    2. 保留以下部分

    ###zyj_starts_提交版

    path: /home/work/zhangyijia/sjms/task1_code/dataset/full_data/   # full_dataset root dir
    train: train/images    # train images (relative to 'path') 
    val: train/images   # val images (relative to 'path') 
    # #test: val/raw/images  # test images (optional)

    # # Classes
    nc: 2  # number of classes
    names: ['car', 'ship']  # class names

    ####zyj_ends_提交版

    #####使用部分训练集训练模型，其余部分测试模型效果（9:1）
    1. 修改'/home/work/zhangyijia/sjms/task1_code/data/DroneVehicle_poly.yaml'
    2. 保留以下部分

    ###zyj_starts_原始的可验证的

    path: /home/work/zhangyijia/sjms/task1_code/dataset/data/   # dataset root dir
    train: train/images    # train images (relative to 'path') 
    val: val/images   # val images (relative to 'path') 
    #test: val/raw/images  # test images (optional)

    # Classes
    nc: 2  # number of classes
    names: ['car', 'ship']  # class names

    ####zyj_ends_原始的可验证的

    ######测试模型

    nohup python -u detect.py --weights '模型地址' \
    --source '测试集图片存放地址' \
    --img 2048 --device 4,5,6,7 --conf-thres 0.25 --iou-thres 0.2 --hide-labels --hide-conf > '日志名' 2>&1 & 

    exp:
    nohup python -u detect.py --weights '/home/work/zhangyijia/sjms/task1_code/runs/train/exp12/weights/best.pt' \
    --source '/home/work/zhangyijia/sjms/datasets/Task1_Test/images/' \
    --img 2048 --device 4,5,6,7 --conf-thres 0.25 --iou-thres 0.2 --hide-labels --hide-conf > log_fulldata/zyj_test_modelsizev7_0907.log 2>&1 & 

    ########计算模型大小
    1. 取消'/home/work/zhangyijia/sjms/task1_code/detect.py'第122和123行的注释
    2. 在'/home/work/zhangyijia/sjms/task1_code/detect.py' 第269行修改计算结果存放的地址
