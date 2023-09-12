import os
import shutil
import random

# 定义数据和标签文件夹的路径
data_folder = "images"
label_folder = "labels"

# 定义训练集和验证集的输出文件夹路径
train_data_folder = "train/images"
train_label_folder = "train/labelTxt"
val_data_folder = "val/images"
val_label_folder = "val/labelTxt"

# 定义训练集和验证集的图片名称记录文件路径
train_txt_path = "train/imgnamefile.txt"
val_txt_path = "val/imgnamefile.txt"

# 设置随机种子以确保每次划分结果一致
random.seed(42)

# 获取所有数据文件的文件名列表
data_files = os.listdir(data_folder)

# 随机打乱文件列表
random.shuffle(data_files)

# 计算训练集和验证集的划分点
split_point = int(0.9 * len(data_files))

# 创建训练集和验证集文件夹
os.makedirs(train_data_folder, exist_ok=True)
os.makedirs(train_label_folder, exist_ok=True)
os.makedirs(val_data_folder, exist_ok=True)
os.makedirs(val_label_folder, exist_ok=True)

# 创建训练集和验证集图片名称记录文件
train_txt = open(train_txt_path, "w")
val_txt = open(val_txt_path, "w")

# 将数据和标签按划分点分配到训练集和验证集
for i, data_file in enumerate(data_files):
    src_data_path = os.path.join(data_folder, data_file)
    src_label_path = os.path.join(label_folder, data_file.replace(".jpg", ".txt"))

    if i < split_point:
        dest_data_folder = train_data_folder
        dest_label_folder = train_label_folder
        txt_file = train_txt
    else:
        dest_data_folder = val_data_folder
        dest_label_folder = val_label_folder
        txt_file = val_txt

    dest_data_path = os.path.join(dest_data_folder, data_file)
    dest_label_path = os.path.join(dest_label_folder, data_file.replace(".jpg", ".txt"))

    # 复制数据和标签文件到相应的文件夹
    shutil.copy(src_data_path, dest_data_path)
    shutil.copy(src_label_path, dest_label_path)

    # 写入图片名称到对应的记录文件
    data_file = data_file.split('.')[0]
    txt_file.write(data_file + "\n")

# 关闭记录文件
train_txt.close()
val_txt.close()

print("数据集划分和记录完成。")
