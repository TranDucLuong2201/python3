import streamlit as st
import pandas as pd

file_path = 'data(fixed).csv'
df = pd.read_csv(file_path, encoding='utf-8')

def data_table(df):
    # Thông tin mô tả và liên kết đến nguồn dữ liệu
    st.markdown("""
    ### Bảng dữ liệu đầu tư trực tiếp nước ngoài (FDI) vào Việt Nam từ 2015 đến 2022
    Nguồn dữ liệu: [Open Development Mekong](https://data.opendevelopmentmekong.net/dataset/fdi-investment-in-vietnam-2015-2022)
    """)

    # Số lượng mục trên mỗi trang
    per_page = 10

    # Tạo thanh trượt để chọn trang
    page_number = st.slider('Trang', 1, (len(df) // per_page) + 1)

    # Lấy dữ liệu cho trang hiện tại
    start = (page_number - 1) * per_page
    end = start + per_page
    page_data = df[start:end]

    # Hiển thị dữ liệu
    st.write(page_data)

data_table(df)