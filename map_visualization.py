import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.title("Biểu đồ bản đồ")
# Đọc dữ liệu từ file CSV
def load_data():
    # Đảm bảo bạn đã tải dữ liệu từ file CSV
    new_df = pd.read_csv('data(fixed).csv')
    new_df['Total number of projects'] = new_df['Total number of projects'].astype(int)
    new_df['Total registered capital (million USD)'] = new_df['Total registered capital (million USD)'].astype(float)
    new_df['Value of capital contribution, share purchase (million USD)'] = new_df['Value of capital contribution, share purchase (million USD)'].astype(float)
    new_df['Total investment (million USD)'] = new_df['Total investment (million USD)'].astype(float)
    return new_df

# Hàm vẽ biểu đồ bản đồ và hiển thị thông tin
def plot_fdi_map(new_df):
    # Xác định phạm vi màu cố định trên tất cả các năm
    zmin = new_df['Total investment (million USD)'].min()
    zmax = new_df['Total investment (million USD)'].max()

    # Dropdown chọn năm
    year = st.selectbox(
        'Select Year',
        options=sorted(new_df['Year'].unique(), reverse=True),
        index=len(new_df['Year'].unique()) - 1
    )

    # Lọc dữ liệu theo năm
    year_data = new_df[new_df['Year'] == year]
    
    # Tính tổng số dự án, tổng vốn đăng ký, giá trị mua cổ phần và tổng số tiền đầu tư
    country_data_year = year_data.groupby('Country').agg({
        'Total number of projects': 'sum',
        'Total registered capital (million USD)': 'sum',
        'Value of capital contribution, share purchase (million USD)': 'sum',
        'Total investment (million USD)': 'sum'
    }).reset_index()

    # Định nghĩa các giá trị chia (bins)
    bins = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500]  # Tùy chỉnh thêm nếu cần
    ticktext = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins)-1)]  # Nhãn hiển thị cho các khoảng

    # Tạo bản đồ choropleth
    fig = go.Figure(data=go.Choropleth(
        locations=country_data_year['Country'],
        locationmode='country names',
        z=country_data_year['Total investment (million USD)'],  # Dữ liệu để tô màu
        hovertext=country_data_year['Country'],
        hovertemplate=(
            'Country: %{location}<br>' +
            'Total Projects: %{customdata[0]}<br>' +
            'Total registered capital: %{customdata[1]:,.2f} million USD<br>' +
            'Capital contribution, share purchase: %{customdata[2]:,.2f} million USD<br>' +
            'Total investment: %{z:,.2f} million USD'
        ),
        customdata=country_data_year[['Total number of projects', 'Total registered capital (million USD)', 'Value of capital contribution, share purchase (million USD)']].values,
        colorbar=dict(
            title="Total Investment (million USD)",
            tickvals=[(bins[i] + bins[i + 1]) / 2 for i in range(len(bins) - 1)],  # Trung tâm mỗi khoảng
            ticktext=ticktext  # Gắn nhãn cho các khoảng chia
        ),
        zmin=bins[0],           # Giá trị nhỏ nhất
        zmax=bins[-1],          # Giá trị lớn nhất
        zauto=False,            # Tắt tự động chia mốc
        colorscale='Viridis_r'  # Bảng màu đảo ngược
    ))

    # Cập nhật bố cục bản đồ
    fig.update_layout(
        geo=dict(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white"),
        title=f'Total investment by Country in {year}'
    )

    # Hiển thị bản đồ và thông tin
    st.plotly_chart(fig)

    # Hiển thị thông tin khi click vào quốc gia
    click_data = st.session_state.get('click_data', None)
    if click_data:
        country_name = click_data['points'][0]['location']
        country_info_text = country_data_year[country_data_year['Country'] == country_name].iloc[0]
        st.write(f"Country: {country_name}")
        st.write(f"Total Projects: {country_info_text['Total number of projects']}")
        st.write(f"Total Registered capital: {country_info_text['Total registered capital (million USD)']:,.2f} million USD")
        st.write(f"Capital contribution, share purchase: {country_info_text['Value of capital contribution, share purchase (million USD)']:,.2f} million USD")
        st.write(f"Total Investment: {country_info_text['Total investment (million USD)']:,.2f} million USD")
    else:
        st.write("Select a country to see details")

# Gọi hàm trong Streamlit
def main():
    new_df = load_data()
    plot_fdi_map(new_df)


main()
