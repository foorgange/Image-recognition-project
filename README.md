# Image-Recognition-Project

基于 **YOLO** 和 **Streamlit** 的 Web 端人工智能目标检测系统  
A web-based AI object detection system using **YOLO** and **Streamlit**

---
注：此项目为很久之前还技术栈薄弱的时候出于学习yolo目的配合ai做的小项目，已很久不维护，且未经过严谨测试，代码仅供学习和参考。

## 项目简介 / Project Overview

这个项目是一个基于 **YOLO**（目标检测模型）和 **Streamlit**（Python Web 框架）的简单但实用的 Web 应用。它支持用户上传图片（或摄像头视频流）进行目标检测，并可视化检测结果。

This project is a lightweight but practical web application built using **YOLO** for object detection and **Streamlit** for the frontend. Users can upload images or stream from a camera to perform object detection, and see the detection results in real time.

---

## 功能 / Features

- 上传静态图片进行目标检测  
- 支持实时摄像头视频流输入（如笔记本摄像头）  
- 可视化检测框 + 置信度 +类别信息  
- 检测参数（如置信度阈值）可调  
- 检测结果保存（截图 / 帧）  
- 日志记录 / 性能统计（可选）  

---

## 项目结构 / Project Structure


├── config/             # 配置相关（如模型配置、参数等）
├── dataSources/        # 存放数据、样本或输入源（如果有）
├── src/                # 项目核心逻辑代码（模型推理、utils 等）
├── main.py             # 后端入口脚本 / 主逻辑脚本
├── run_frontend.py     # 启动 Streamlit 前端的脚本
├── requirements.txt    # 所需 Python 包
└── README.md           # 项目说明（就是这个文件）

---

## 技术栈 / Tech Stack

- **Python** — 主要编程语言  
- **PyTorch** — 用于加载和推理 YOLO 模型  
- **YOLO** — 目标检测算法（如 YOLOv5）  
- **Streamlit** — 构建 Web 前端、界面展示  
- **OpenCV** — 图像处理（读取、绘制框等）  
- **Pandas**（可选） — 用于日志或结果数据统计处理  

---

## 安装与运行 / Installation & Run

下面是一个典型的安装 + 启动流程（假设你使用 venv 或者别的虚拟环境）：


# 克隆仓库
git clone https://github.com/foorgange/Image-recognition-project.git
cd Image-recognition-project

# 创建并激活虚拟环境（示例：venv）
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# .\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行 Streamlit 前端
python run_frontend.py

Streamlit 默认会在 localhost:8501 启动。打开浏览器访问即可。

使用方式 / Usage


打开浏览器，访问本地 Streamlit 页面


在页面中选择 “上传图片” 或 “启用摄像头流”


上传 / 切换输入源后，页面会显示带有检测框的图片 / 视频帧


可调整置信度（confidence threshold）等参数，以控制检测灵敏度


可通过提供按钮或脚本保存检测结果（例如截图）



模型权重 / Model Weights


提示：建议不要将 .pt（或其他大型模型权重）文件直接提交到 GitHub。


你可以把模型权重放在云存储（如 Google Drive、百度云、S3 等），然后在代码中配置从外部下载，或者使用 Git LFS。


如果你已有权重文件，请在 config/（或你指定的路径）下放一个下载脚本 / 指向权重的说明。

配置文件 / Configuration


config/ 目录中用于存放模型配置（如 YOLO 的 yaml 文件）、阈值、类别名称等。


你可以新增一个 config.yaml 或类似文件，来统一管理各种可调超参。



