import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

new_file_path = 'fdi_country_partners_en(fixed).csv'
new_data = pd.read_csv(new_file_path)

new_df = pd.DataFrame(new_data)

new_df['Total number of projects'] = new_df['Total number of projects'].astype(int)
new_df['Total registered capital (million USD)'] = new_df['Total registered capital (million USD)'].astype(float)
new_df['Value of capital contribution, share purchase (million USD)'] = new_df['Value of capital contribution, share purchase (million USD)'].astype(float)
new_df['Total investment (million USD)'] = new_df['Total investment (million USD)'].astype(float)

# Xác định phạm vi màu cố định trên tất cả các năm
zmin = new_df['Total investment (million USD)'].min()
zmax = new_df['Total investment (million USD)'].max()

app = dash.Dash(__name__)

# Dropdown năm
year_dropdown = dcc.Dropdown(
    id='year-dropdown',
    options=[{'label': str(year), 'value': year} for year in new_df['Year'].unique()],
    value=2022,  # Mặc định chọn năm 2022
    style={'width': '50%'}
)

# Bản đồ 3D
map_graph = dcc.Graph(id='map-graph')

# Mô tả thông tin khi click vào quốc gia
country_info = html.Div(id='country-info', style={'padding': '10px'})

# Giao diện người dùng
app.layout = html.Div([
    year_dropdown,
    map_graph,
    country_info  # Thêm phần hiển thị thông tin
])

# Cập nhật bản đồ theo năm chọn
@app.callback(
    Output('map-graph', 'figure'),
    Output('country-info', 'children'),
    [Input('year-dropdown', 'value'),
     Input('map-graph', 'clickData')]
)
def update_map(year, click_data):
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

    fig = go.Figure(data=go.Choropleth(
        locations=country_data_year['Country'],
        locationmode='country names',
        z=country_data_year['Total investment (million USD)'],  # Dữ liệu để tô màu
        hovertext=country_data_year['Country'],
        hovertemplate=(  # Thông tin khi hover
            'Country: %{location}<br>' +
            'Total Projects: %{customdata[0]}<br>' +
            'Total registered capital: %{customdata[1]:,.2f} million USD<br>' +
            'Capital contribution, share purchase: %{customdata[2]:,.2f} million USD<br>'
            'Total investment: %{z:,.2f} million USD'
        ),
        customdata=country_data_year[['Total number of projects', 'Total registered capital (million USD)', 'Value of capital contribution, share purchase (million USD)']].values,
        colorbar=dict(
            title="Total Investment ( million USD )",
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
        title=f'Total investment by Country in {year}',
        scene=dict(
            zaxis=dict(title='Total Investment', range=[0, zmax + 100]),
            camera=dict(
                eye=dict(x=2, y=2, z=2)
            )
        )
    )

    # Hiển thị thông tin khi click vào quốc gia
    if click_data:
        country_name = click_data['points'][0]['location']
        country_info_text = country_data_year[country_data_year['Country'] == country_name].iloc[0]
        country_info = html.Div([
            html.H4(f"Country: {country_name}"),
            html.P(f"Total Projects: {country_info_text['Total number of projects']}"),
            html.P(f"Total Registered capital: {country_info_text['Total registered capital (million USD)']:,.2f} million USD"),
            html.P(f"Capital contribution, share purchase: {country_info_text['Value of capital contribution, share purchase (million USD)']:,.2f} million USD"),
            html.P(f"Total Investment: {country_info_text['Total investment (million USD)']:,.2f} million USD")
        ])
    else:
        country_info = html.Div([
            html.H4("Select a country to see details")
        ])

    return fig, country_info

if __name__ == '__main__':
    app.run_server(debug=True)