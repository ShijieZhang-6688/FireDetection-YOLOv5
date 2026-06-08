# YOLOv5 火焰检测论文复刻记录

作者署名：shijie zhang

## 复刻目标

本项目复刻参考文档 `FireDetection_23.docx` 中的 YOLOv5 火焰检测实验。参考文档的原署名有误，本仓库统一使用 `shijie zhang`。

目标不是整理旧项目，而是从官方 YOLOv5 代码、论文记录的数据集和可复现训练命令重新构建。

## 论文记录的关键配置

| 项目 | 配置 |
| --- | --- |
| 模型 | YOLOv5n |
| 类别 | `fire` |
| 数据集 | Roboflow `yolo-j5nit/fire-detect-i7huf-0g2xe`, version 1 |
| 数据量 | train 约 2026, valid 约 570, test 约 290 |
| 输入尺寸 | 640 |
| batch size | 24 |
| epochs | 300 |
| optimizer | SGD |
| 初始学习率 | `lr0=0.01` |
| 权重衰减 | `weight_decay=5e-5` |
| 论文结果描述 | 火焰检测精度约 74%，并展示 mAP、PR、F1 和混淆矩阵 |

## 环境准备

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

如果使用 GPU，请根据本机 CUDA 版本从 PyTorch 官网安装匹配的 `torch` 和 `torchvision`。

本仓库已兼容 PyTorch 2.6+ 的 checkpoint 加载行为：YOLOv5 v7.0 的完整模型 checkpoint 需要用 `weights_only=False` 加载。只对受信任的官方权重或本项目训练权重使用该路径。

## 数据集下载

Roboflow 下载通常需要 API key。不要把 API key 写入 Git。

```powershell
$env:ROBOFLOW_API_KEY="your_key_here"
python scripts/download_dataset.py
python scripts/validate_dataset.py
```

下载后预期目录：

```text
datasets/fire-detect-1/
  train/images
  train/labels
  valid/images
  valid/labels
  test/images
  test/labels
```

## 训练

论文写明 `weight_decay=5e-5`，因此训练时使用本项目新增的 `data/hyps/hyp.fire.yaml`。

```powershell
python train.py --img 640 --batch 24 --epochs 300 --data data/fire.yaml --cfg models/yolov5n.yaml --weights yolov5n.pt --optimizer SGD --hyp data/hyps/hyp.fire.yaml --name fire_yolov5n_repro
```

如果显存不足，先将 `--batch 24` 降到 `16`、`8` 或 `4` 做冒烟验证；正式复刻结果仍应记录实际 batch。

## 验证和推理

```powershell
python val.py --weights runs/train/fire_yolov5n_repro/weights/best.pt --data data/fire.yaml --img 640
python detect.py --weights runs/train/fire_yolov5n_repro/weights/best.pt --source path/to/images_or_video --img 640 --conf 0.25
```

## 结果记录

正式训练完成后，在 README 中补充：

- Precision
- Recall
- mAP@0.5
- mAP@0.5:0.95
- `results.png`
- `confusion_matrix.png`
- PR/F1 曲线

权重、数据集和训练输出不要提交到 GitHub。
