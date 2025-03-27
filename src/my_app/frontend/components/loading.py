import streamlit as st

def show_loading_animation():
    st.markdown("""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <style>
            .loading-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100px;
            }
            
            .loading-spinner {
                width: 50px;
                height: 50px;
                border: 5px solid #f3f3f3;
                border-top: 5px solid #2196f3;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </div>
    """, unsafe_allow_html=True) 