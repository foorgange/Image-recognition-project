import streamlit as st
import cv2
import tempfile
import os
from pathlib import Path
import time
import numpy as np
from PIL import Image
import pandas as pd
from datetime import datetime

from ..models.yolo_model import YOLOModel
from ..utils.config_loader import load_config
from ..reports.visualization import DetectionVisualizer
from ..reports.metrics import DetectionMetrics

class StreamlitApp:
    def __init__(self):
        self.setup_page_config()
        self.config = load_config()
        self.apply_custom_css()
        self.initialize_session_state()

    def setup_page_config(self):
        """设置页面配置"""
        st.set_page_config(
            page_title="AI Vision System",
            page_icon="🎯",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def apply_custom_css(self):
        """应用自定义CSS样式"""
        st.markdown("""
        <style>
        /* 主题颜色 */
        :root {
            --primary-bg: #0B1121;
            --secondary-bg: #162447;
            --accent-color: #1E88E5;
            --text-color: #E0E0E0;
            --card-bg: #1A1F35;
        }
        
        /* 全局样式 */
        .stApp {
            background: linear-gradient(135deg, var(--primary-bg) 0%, var(--secondary-bg) 100%);
            color: var(--text-color);
        }
        
        /* 侧边栏样式 */
        .css-1d391kg {
            background-color: var(--card-bg);
        }
        
        /* 卡片样式 */
        .card {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
        }
        
        /* 标题样式 */
        h1 {
            background: linear-gradient(90deg, #1E88E5, #64B5F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        }
        
        h2, h3 {
            color: var(--text-color);
            font-weight: 500;
        }
        
        /* 按钮样式 */
        .stButton>button {
            background: linear-gradient(90deg, #1E88E5, #64B5F6);
            color: white;
            border: none;
            padding: 0.5rem 2rem;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
        }
        
        /* 指标卡片样式 */
        .metric-card {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E88E5;
            margin: 0.5rem 0;
        }
        
        .metric-label {
            color: var(--text-color);
            font-size: 1rem;
            opacity: 0.8;
        }
        
        /* 进度条样式 */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #1E88E5, #64B5F6);
        }
        
        /* 选择器样式 */
        .stSelectbox > div > div {
            background-color: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* 图表样式 */
        .stPlot {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 1rem;
        }
        
        /* 动画效果 */
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(30, 136, 229, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(30, 136, 229, 0); }
            100% { box-shadow: 0 0 0 0 rgba(30, 136, 229, 0); }
        }
        
        .detection-active {
            animation: pulse 2s infinite;
        }
        
        /* 上传区域样式 */
        .uploadfile {
            border: 2px dashed rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .uploadfile:hover {
            border-color: var(--accent-color);
        }
        
        /* 表格样式 */
        .dataframe {
            background: var(--card-bg);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)

    def initialize_session_state(self):
        """初始化会话状态"""
        if 'model' not in st.session_state:
            st.session_state.model = None
        if 'metrics' not in st.session_state:
            st.session_state.metrics = DetectionMetrics()
        if 'running' not in st.session_state:
            st.session_state.running = False

    def run(self):
        """运行Streamlit应用"""
        self.render_header()
        
        # 创建标签页
        tabs = st.tabs([
            "🎥 Real-time Detection",
            "🖼️ Image Analysis",
            "📊 Analytics Dashboard"
        ])
        
        with tabs[0]:
            self.render_realtime_detection()
        with tabs[1]:
            self.render_image_detection()
        with tabs[2]:
            self.render_analytics()

    def render_header(self):
        """渲染页面头部"""
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1>AI Vision System</h1>
            <p style="color: #64B5F6; font-size: 1.2rem;">
                Advanced Object Detection & Analytics
            </p>
        </div>
        """, unsafe_allow_html=True)

    def render_metric_card(self, title, value, icon):
        """渲染指标卡片"""
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; color: #64B5F6; margin-bottom: 0.5rem;">
                {icon}
            </div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{title}</div>
        </div>
        """, unsafe_allow_html=True)

    def render_realtime_detection(self):
        """渲染实时检测页面"""
        col1, col2 = st.columns([7, 3])
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            video_placeholder = st.empty()
            
            # 添加状态指示器
            if st.session_state.running:
                st.markdown("""
                    <div style="text-align: center; color: #1E88E5;">
                        🔴 Detection Running
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Control Panel")
            source = st.radio(
                "Select Input Source",
                ["📹 Camera", "📁 Video File"],
                key="source_select"
            )
            
            if source == "📹 Camera":
                camera_id = st.selectbox("Select Camera", [0, 1, 2])
                self.run_camera_detection(camera_id, video_placeholder)
            else:
                st.markdown('<div class="uploadfile">', unsafe_allow_html=True)
                video_file = st.file_uploader(
                    "Drop your video file here",
                    type=['mp4', 'avi', 'mov']
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                if video_file:
                    self.run_video_detection(video_file, video_placeholder)
                    
            st.markdown('</div>', unsafe_allow_html=True)

    def render_image_detection(self):
        """渲染图片检测页面"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Image Analysis")
        
        upload_col, preview_col = st.columns(2)
        
        with upload_col:
            st.markdown('<div class="uploadfile">', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Drop your image here",
                type=['jpg', 'jpeg', 'png']
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        if uploaded_file:
            image = Image.open(uploaded_file)
            preview_col.image(image, caption="Preview", use_column_width=True)
            
            if st.button("🔍 Analyze Image"):
                with st.spinner("Processing..."):
                    result_image = self.process_image(uploaded_file)
                    st.image(result_image, caption="Detection Result")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def render_analytics(self):
        """渲染分析页面"""
        if st.session_state.metrics:
            metrics = st.session_state.metrics.get_summary()
            
            # 显示关键指标
            col1, col2, col3 = st.columns(3)
            with col1:
                self.render_metric_card(
                    "Total Frames",
                    metrics['total_frames'],
                    "🎞️"
                )
            with col2:
                self.render_metric_card(
                    "Average FPS",
                    f"{metrics['average_fps']:.1f}",
                    "⚡"
                )
            with col3:
                self.render_metric_card(
                    "Objects Detected",
                    metrics['total_detections'],
                    "🎯"
                )
            
            # 显示图表
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Detection Distribution")
            if metrics['class_distribution']:
                chart_data = pd.DataFrame.from_dict(
                    metrics['class_distribution'],
                    orient='index',
                    columns=['count']
                )
                st.bar_chart(chart_data)
            st.markdown('</div>', unsafe_allow_html=True)

    def process_image(self, image_file):
        """处理单张图片"""
        if st.session_state.model is None:
            st.session_state.model = YOLOModel(self.config['model'])
        
        image = Image.open(image_file)
        image = np.array(image)
        
        detections = st.session_state.model.predict(image)
        visualizer = DetectionVisualizer()
        
        return visualizer.draw_detections(image, detections)

    def run_camera_detection(self, camera_id, placeholder):
        """运行摄像头检测"""
        cap = cv2.VideoCapture(camera_id)
        visualizer = DetectionVisualizer()
        
        if st.session_state.model is None:
            st.session_state.model = YOLOModel(self.config['model'])
        
        # 创建两列布局用于开始和停止按钮
        col1, col2 = st.columns(2)
        
        with col1:
            start_button = st.button("▶️ Start")
        with col2:
            stop_button = st.button("⏹️ Stop")
            
        if start_button:
            st.session_state.running = True
            
        if stop_button:
            st.session_state.running = False
            
        try:
            while st.session_state.running:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                detections = st.session_state.model.predict(frame)
                
                if detections is not None:
                    frame = visualizer.draw_detections(frame, detections)
                
                placeholder.image(frame)
                
        finally:
            cap.release()
            st.session_state.running = False

    def run_video_detection(self, video_file, placeholder):
        """运行视频文件检测"""
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        
        cap = cv2.VideoCapture(tfile.name)
        visualizer = DetectionVisualizer()
        
        if st.session_state.model is None:
            st.session_state.model = YOLOModel(self.config['model'])
        
        # 创建两列布局用于开始和停止按钮
        col1, col2 = st.columns(2)
        
        with col1:
            start_button = st.button("▶️ Start")
        with col2:
            stop_button = st.button("⏹️ Stop")
            
        if start_button:
            st.session_state.running = True
            
        if stop_button:
            st.session_state.running = False
            
        try:
            while st.session_state.running:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                detections = st.session_state.model.predict(frame)
                
                if detections is not None:
                    frame = visualizer.draw_detections(frame, detections)
                
                placeholder.image(frame)
                
        finally:
            cap.release()
            os.unlink(tfile.name)
            st.session_state.running = False 