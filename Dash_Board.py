import streamlit as st

logo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6B66TcJjm2QDGBJ1QgL-XgNAGLn6e6uNqSA&s"
st.set_page_config(page_title='FDI - VIETNAM', layout='wide', page_icon=logo)

pages = {
    "Contents": [
        st.Page("Overview.py", title="Tổng quan"),
        st.Page("Charts.py", title="Biểu đồ thống kê"),
        st.Page("map_visualization.py", title="Biểu đồ bản đồ"),
    ],
    "Resources": [
        st.Page("Data_Table.py", title="Bảng dữ liệu"),
    ],
}

pg = st.navigation(pages)
pg.run()