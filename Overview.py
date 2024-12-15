import streamlit as st
import pandas as pd
from visualizations import (
    plot_new_projects_by_year,
    plot_registered_capital_by_year,
    plot_top_countries_by_projects,
    plot_top_countries_by_registered_capital,
    plot_total_projects_and_investment_by_year,
    plot_top_countries_by_total_investment,
    plot_pie_chart_top_countries_by_projects,
    plot_pie_chart_top_countries_by_registered_capital,
    plot_pie_chart_top_countries_by_total_investment,
    plot_top_10_projects_2022,
    plot_top_10_registered_capital_2022
)

def overview():
    # CSS để tùy chỉnh phần header và tiêu đề
    st.markdown(
        """
        <style>
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: white; /* Nền trắng */
            padding: 10px;
            border-radius: 5px;
        }
        .header img {
            max-height: 50px; /* Chiều cao tối đa của ảnh */
            margin-right: 20px; /* Khoảng cách giữa ảnh và chữ */
        }
        .header h1 {
            font-size: 24px;
            color: black; /* Màu chữ đen */
        }
        .title {
            text-align: center;
            color: red; /* Màu chữ đỏ */
            font-size: 32px; /* Kích thước chữ */
            margin-top: 20px;
            text-transform: uppercase; /* In hoa chữ */
            font-weight: bold; /* In đậm chữ */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # HTML để tạo header
    st.markdown(
        """
        <div class="header">
            <img src="https://phys.hcmus.edu.vn/uploads/khoa-vat-ly/logo_Khoa/vi_phys.png" alt="Logo">
            <h1>BỘ MÔN VẬT LÝ TIN HỌC</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # HTML để tạo tiêu đề
    st.markdown(
        """
        <div class="title">
            PHÂN TÍCH DỮ LIỆU ĐÓNG GÓP CỦA ĐẦU TƯ TRỰC TIẾP NƯỚC NGOÀI ĐỐI VỚI KINH TẾ VIỆT NAM GIAI ĐOẠN 2015-2022
        </div>
        """,
        unsafe_allow_html=True
    )

    # Hiển thị các biểu đồ tổng quan
    st.subheader("Tổng quan về số lượng dự án và vốn đầu tư")
    col1, col2 = st.columns(2)
    with col1:
        plot_new_projects_by_year(df)
    with col2:
        plot_registered_capital_by_year(df)

    st.subheader("Top 10 quốc gia theo số lượng dự án và vốn đăng ký")
    col3, col4 = st.columns(2)
    with col3:
        plot_top_countries_by_projects(df)
    with col4:
        plot_top_countries_by_registered_capital(df)

    st.subheader("Tổng số dự án và tổng vốn đầu tư theo năm")
    plot_total_projects_and_investment_by_year(df)

    st.subheader("Top 10 quốc gia theo tổng số tiền đầu tư")
    plot_top_countries_by_total_investment(df)

    st.subheader("Biểu đồ tròn biểu diễn tỷ lệ của tổng dự án, vốn đăng ký và tổng số tiền đầu tư")
    col5, col6, col7 = st.columns(3)
    with col5:
        plot_pie_chart_top_countries_by_projects(df)
    with col6:
        plot_pie_chart_top_countries_by_registered_capital(df)
    with col7:
        plot_pie_chart_top_countries_by_total_investment(df)

    st.subheader("Top 10 quốc gia theo tổng số dự án và vốn đăng ký năm 2022")
    col8, col9 = st.columns(2)
    with col8:
        plot_top_10_projects_2022(df)
    with col9:
        plot_top_10_registered_capital_2022(df)

# Đọc dữ liệu từ tệp CSV
file_path = 'data(fixed).csv'
df = pd.read_csv(file_path, encoding='utf-8')

# Gọi hàm overview để hiển thị tổng quan
overview()
