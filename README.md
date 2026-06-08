# FireDetection-YOLOv5

基于 YOLOv5n 的火焰检测论文复刻项目。

作者：shijie zhang

本仓库从官方 YOLOv5 v7.0 代码重新搭建，用于复刻参考论文中的火焰检测实验。项目不复用旧工程内容，数据集按论文记录重新从 Roboflow 获取，训练参数尽量对齐论文设置。

## 项目目标

- 使用 YOLOv5n 训练单类别火焰检测模型。
- 使用论文记录的 Roboflow `fire-detect` 数据集。
- 复现 640 输入尺寸、batch 24、300 epochs、SGD、`lr0=0.01`、`weight_decay=5e-5` 的训练流程。
- 记录 Precision、Recall、mAP、PR 曲线、F1 曲线和混淆矩阵。

## 代码来源

本项目基于 Ultralytics YOLOv5 v7.0：

- GitHub: https://github.com/ultralytics/yolov5
- License: GPL-3.0，见 [LICENSE](LICENSE)

本地重建时，GitHub 直连不稳定，因此源码通过 SourceForge 的 YOLOv5 exact mirror 下载，版本对应 GitHub tag `v7.0` / commit `915bbf2`。

## 环境安装

建议使用 Python 3.8+。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

如果使用 GPU，请先根据 CUDA 版本安装匹配的 PyTorch。

当前仓库对 YOLOv5 v7.0 做了一个小兼容补丁：在 PyTorch 2.6+ 默认 `weights_only=True` 的环境下，显式用 `weights_only=False` 加载受信任的 YOLOv5 checkpoint。这样可以正常加载官方 `yolov5n.pt` 和本项目训练出的 `best.pt`。

## 数据集

论文记录的数据集：

https://universe.roboflow.com/yolo-j5nit/fire-detect-i7huf-0g2xe/dataset/1

预期规模：

- train: 约 2026 张
- valid: 约 570 张
- test: 292 张
- class: `fire`

Roboflow 下载需要 API key：

```powershell
$env:ROBOFLOW_API_KEY="your_key_here"
python scripts/download_dataset.py
python scripts/validate_dataset.py
```

下载后的数据集会放在 `datasets/fire-detect-1/`，该目录不会提交到 Git。

## 训练

正式复刻命令：

```powershell
python train.py --img 640 --batch 24 --epochs 300 --data data/fire.yaml --cfg models/yolov5n.yaml --weights yolov5n.pt --optimizer SGD --hyp data/hyps/hyp.fire.yaml --name fire_yolov5n_repro
```

说明：

- `data/fire.yaml` 定义单类别火焰数据集。
- `data/hyps/hyp.fire.yaml` 将 `weight_decay` 设置为论文中的 `5e-5`。
- `yolov5n.pt` 会由 YOLOv5 在训练时自动下载；如果网络不可用，可手动下载后放到项目根目录。

快速冒烟测试可以先运行 1 个 epoch：

```powershell
python train.py --img 640 --batch 4 --epochs 1 --data data/fire.yaml --cfg models/yolov5n.yaml --weights yolov5n.pt --optimizer SGD --hyp data/hyps/hyp.fire.yaml --name smoke_fire_yolov5n
```

## 验证和推理

```powershell
python val.py --weights runs/train/fire_yolov5n_repro/weights/best.pt --data data/fire.yaml --img 640
python detect.py --weights runs/train/fire_yolov5n_repro/weights/best.pt --source path/to/images_or_video --img 640 --conf 0.25
```

## 复刻结果

正式 300 epochs 训练完成后，在这里补充最终指标：

| 指标 | 结果 |
| --- | --- |
| Precision | TBD |
| Recall | TBD |
| mAP@0.5 | TBD |
| mAP@0.5:0.95 | TBD |

论文描述火焰检测精度约为 74%。最终结果需要结合相同数据集版本、训练设备、随机种子和实际 batch size 解释。

## 更多记录

复刻参数、数据集说明和结果记录模板见 [docs/reproduction.md](docs/reproduction.md)。
