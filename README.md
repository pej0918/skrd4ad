# Skip-Connected Reverse Distillation for Robust One-Class Anomaly Detection

[![CVPR 2025 Workshop](https://img.shields.io/badge/CVPR%202025-Workshop-orange)](https://cvpr2025.thecvf.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![PyTorch](https://img.shields.io/badge/framework-PyTorch-red)](https://pytorch.org/)
[![MVTec-AD](https://img.shields.io/badge/dataset-MVTec--AD-green)](https://www.mvtec.com/company/research/datasets/mvtec-ad/)
[![VAD](https://img.shields.io/badge/dataset-VAD-brightgreen)](https://github.com/valeoai/VAD)
[![VisA](https://img.shields.io/badge/dataset-VisA-yellow)](https://github.com/amazon-science/spot-diff)

> 📣 Accepted at **CVPR 2025 Workshop (VAND 3.0)**  
> 🔧 Official PyTorch implementation of our paper, SK-RD4AD.

## 📖 Introduction

SK-RD4AD (Skip-Connected Reverse Distillation for Anomaly Detection) introduces a novel and effective architecture for one-class anomaly detection. By leveraging non-corresponding skip connections within a reverse knowledge distillation framework, SK-RD4AD effectively mitigates deep feature degradation, a common issue in traditional distillation-based methods. This enhancement significantly improves both pixel-level anomaly localization and image-level detection across various industrial domains.

## 🔥 Key Features
- 🔗 **Non-Corresponding Skip Connections**  
  Enhances multi-scale feature propagation between encoder and decoder, allowing both low-level textures and high-level semantics to be preserved.

- 🚀 **State-of-the-Art Performance**  
  Surpasses RD4AD on **MVTec-AD**, **VisA**, and **VAD** by up to **+3.5% AUROC**, **+21% AUPRO**, and excels in challenging categories like **Transistor**.

- 🌐 **Generalization Power**  
  Effectively handles diverse anomaly types and generalizes to **real-world datasets** such as **automotive VAD** and **industrial VisA**.

- ⚙️ **Efficient Architecture**  
  Lightweight decoder with modest memory (401MB) and inference time (0.37s), making it suitable for **edge and cloud** deployment.

---


## 📂 Model Overview
SK-RD4AD enhances the original RD4AD framework by addressing deep-layer information loss. It introduces strategically designed non-corresponding skip connections that allow features from shallower teacher layers to influence deeper student layers. This architecture improves the decoder’s capacity to reconstruct complex features and leads to significantly better anomaly localization performance.


![image](https://github.com/user-attachments/assets/51916259-a0a4-4d39-aaa0-ee170d87cfe6)


## ⚙️ Experiment Settings

### 🧪 Installation
```bash
pip install -r requirements.txt
```

### 📁 Dataset Preparation
Download the MVTec, VAD and VisA datasets from:
- [MVTec AD Dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad/)
- [Valeo Anomaly Dataset (VAD)](https://drive.google.com/file/d/1LbHHJHCdkvhzVqekAIRdWjBWaBHxPjuu/view/)
- [visA Dataset](https://github.com/amazon-science/spot-diff)

### 🏃 Train and Test the Model
To train and evaluate the model, use the appropriate script depending on the dataset.

The following command is for training and evaluating the model on **MVTec-AD** :
```bash
python main.py \
    --epochs 200 \
    --res 3 \
    --learning_rate 0.005 \
    --batch_size 16 \
    --seed 111 \
    --class all \
    --seg 1 \
    --print_epoch 10 \
    --data_path /home/user/mvtec/ \
    --save_path /home/user/anomaly_checkpoints/skipconnection/ \
    --print_loss 1 \
    --net wide_res50 \
    --L2 0
```
> For **VisA**, use `main_visa.py`.
> For **VAD**, use `main_vad.py`.

## 📈 Performance Highlights
The model is evaluated using AUROC and AUPRO metrics at pixel level. SK-RD4AD consistently shows significant improvements over RD4AD across MVTec-AD, Valeo VAD, and VisA datasets, especially in categories requiring fine-grained spatial reasoning. : 

### MVTec-AD Dataset Performance
| Category     | RD4AD (Pixel AUROC/AUPRO) | SK-RD4AD (Pixel AUROC/AUPRO)   |
|--------------|----------------------------|--------------------------------|
| Carpet       | 98.9 / 97.0                | **99.2 / 97.7**                |
| Bottle       | 98.7 / 96.6                | **98.8 / 96.9**                |
| Hazelnut     | 98.9 / 95.5                | **99.1 / 96.2**                |
| Leather      | 99.4 / 99.1                | **99.6 / 99.2**                |
| **Total Avg**| 97.8 / 93.9                | **98.06 / 94.69**              |

### Valeo Anomaly Dataset (VAD) Performance
| Setting   | Baseline AUROC | SK-RD4AD AUROC |
|-----------|----------------|----------------|
| One-Class | 84.5           | **87.0**       |

### VisA Dataset Performance
| Category     | RD4AD (Pixel AUROC / AUPRO) | SK-RD4AD (Pixel AUROC / AUPRO) |
|--------------|-----------------------------|--------------------------------|
| PCB1         | 99.6 / 43.2                 | 99.6 / **93.7**                |
| PCB2         | 98.3 / 46.4                 | 98.3 / **89.2**                |
| PCB3         | 99.3 / 80.3                 | 98.3 / **90.3**                |
| PCB4         | 98.2 / 72.2                 | **98.6 / 89.0**                |
| Pipe Fryum   | 99.1 / 68.3                 | 99.1 / **94.8**                |
| **Total Avg** | 97.8 / 70.9                 | **98.5 / 92.1**                |

### Model Complexity

| Model       | Time (s) | Memory (MB) | AUROC |
|-------------|----------|-------------|--------|
| RD4AD       | 0.31     | 352         | 97.3   |
| **SK-RD4AD** | 0.37     | 401         | **98.06** |

> Slight increase in cost yields **substantial performance boost**.

## 🖼️ Visualization
<p align="center">
  <img src="https://github.com/user-attachments/assets/b2fe4e4b-6a4c-4c86-8caa-ebef8da92dd8" alt="figg3" width="45%">
  <img src="https://github.com/user-attachments/assets/dbbd9d8a-f70a-4a8f-9a9b-49e2f95ed4be" alt="ffig2" width="45%">

</p>

The visualization results demonstrate **the effectiveness of the SK-RD4AD model in detecting anomalies**. The anomaly maps highlight areas where the model identifies potential defects, using red and yellow hues to indicate regions of high confidence. The overlaid images combine the original images with the anomaly maps, clearly showing the detected anomalies' locations.

## 🎯 Conclusion
SK-RD4AD addresses the challenge of deep feature loss in anomaly detection by introducing **non-corresponding skip connections** within a reverse distillation framework.  
This design improves **multi-scale feature retention** and enhances the model's ability to detect **subtle and diverse anomalies**.  
Tested across industrial benchmarks, it shows consistent improvements over RD4AD, making it a **robust and effective solution for real-world anomaly detection tasks**.

## 📚 Citation

```
TBD
```
## 🙏 Acknowledgement

This work builds upon the [RD4AD (Anomaly Detection via Reverse Distillation From One-Class Embedding)](https://github.com/hq-deng/RD4AD) framework.  
We sincerely thank the original authors for open-sourcing their code and pre-trained models, which made this research possible.



