import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

print("Python path:", sys.path)
print("Project root:", project_root)

os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning'

import streamlit as st
from src.my_app.frontend.app import StreamlitApp

if __name__ == "__main__":
    app = StreamlitApp()
    app.run() 