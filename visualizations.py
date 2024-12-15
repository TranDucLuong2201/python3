import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

# Load and clean data
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    df.replace(' -   ', pd.NA, inplace=True)
    df.fillna(0, inplace=True)
    df.rename(columns={'Value of capital contribution, share purchase\\n(million USD)': 'Value of capital contribution, share purchase (million USD)'}, inplace=True)
    country_mapping = {
        'Liên bang Nga': 'Russia',
        'Federal Republic of Russia': 'Russia',
        "Côte d'Ivoire": "Cote deIvoire",
        "Cu Ba": "Cuba",
        "Nauy": "Norway"
    }
    df['Country'] = df['Country'].str.strip()
    df['Country'] = df['Country'].replace(country_mapping)
    columns_to_convert = ['Newly registered capital (million USD)', 'Adjusted capital (million USD)', 'Value of capital contribution, share purchase (million USD)']
    for col in columns_to_convert:
        df[col] = (
            df[col].astype(str)
            .str.replace('[()]', '', regex=True)
            .str.replace(',', '')
            .apply(lambda x: -float(x) if '(' in x else float(x))
        )
    df['Number of new projects'] = df['Number of new projects'].astype(float).astype(int)
    df['Adjusted project number'] = df['Adjusted project number'].astype(float).astype(int)
    df['Number of times of capital contribution to buy shares'] = (
        df['Number of times of capital contribution to buy shares']
        .astype(str)
        .str.replace('[, ]', '', regex=True)
        .apply(pd.to_numeric, errors='coerce')
        .fillna(0)
        .astype(int)
    )
    df['Total number of projects'] = df['Number of new projects'] + df['Adjusted project number']
    df['Total registered capital (million USD)'] = df['Newly registered capital (million USD)'] + df['Adjusted capital (million USD)']
    df['Total investment (million USD)'] = df['Total registered capital (million USD)'] + df['Value of capital contribution, share purchase (million USD)']
    return df

# Load data
file_path = 'data(fixed).csv'
df = load_and_clean_data(file_path)

def plot_new_projects_by_year(df):
    if 'Year' in df.columns and 'Number of new projects' in df.columns:
        data = df.groupby('Year').agg({'Number of new projects': 'sum'}).reset_index()
        fig = px.line(data, x='Year', y='Number of new projects', title='Số dự án mới theo năm')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Year' và 'Number of new projects'")

def plot_registered_capital_by_year(df):
    if 'Year' in df.columns and 'Newly registered capital (million USD)' in df.columns:
        data = df.groupby('Year').agg({'Newly registered capital (million USD)': 'sum'}).reset_index()
        fig = px.line(data, x='Year', y='Newly registered capital (million USD)', title='Vốn đăng ký theo năm')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Year' và 'Newly registered capital (million USD)'")

def plot_top_countries_by_projects(df):
    if 'Country' in df.columns and 'Number of new projects' in df.columns:
        country_data = df.groupby('Country').agg({'Number of new projects': 'sum'}).reset_index()
        top_countries = country_data.nlargest(10, 'Number of new projects')
        fig = px.bar(top_countries, x='Number of new projects', y='Country', orientation='h', title='Các quốc gia hàng đầu theo số dự án')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Country' và 'Number of new projects'")

def plot_top_countries_by_registered_capital(df):
    if 'Country' in df.columns and 'Newly registered capital (million USD)' in df.columns:
        country_data = df.groupby('Country').agg({'Newly registered capital (million USD)': 'sum'}).reset_index()
        top_countries = country_data.nlargest(10, 'Newly registered capital (million USD)')
        fig = px.bar(top_countries, x='Newly registered capital (million USD)', y='Country', orientation='h', title='Các quốc gia hàng đầu theo vốn đăng ký')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Country' và 'Newly registered capital (million USD)'")

def plot_total_projects_and_investment_by_year(df):
    if 'Year' in df.columns and 'Number of new projects' in df.columns and 'Newly registered capital (million USD)' in df.columns:
        data = df.groupby('Year').agg({'Number of new projects': 'sum', 'Newly registered capital (million USD)': 'sum'}).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data['Year'], y=data['Number of new projects'], name='Dự án'))
        fig.add_trace(go.Line(x=data['Year'], y=data['Newly registered capital (million USD)'], name='Vốn đăng ký'))
        fig.update_layout(title='Tổng số dự án và vốn đầu tư theo năm', xaxis_title='Năm', yaxis_title='Số lượng / Triệu USD')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Year', 'Number of new projects', và 'Newly registered capital (million USD)'")

def plot_top_countries_by_total_investment(df):
    if 'Country' in df.columns and 'Total investment (million USD)' in df.columns:
        country_data = df.groupby('Country').agg({'Total investment (million USD)': 'sum'}).reset_index()
        top_countries = country_data.nlargest(10, 'Total investment (million USD)')
        fig = px.bar(top_countries, x='Total investment (million USD)', y='Country', orientation='h', title='Các quốc gia hàng đầu theo tổng vốn đầu tư')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Country' và 'Total investment (million USD)'")

def plot_pie_chart_top_countries_by_projects(df):
    if 'Country' in df.columns and 'Number of new projects' in df.columns:
        country_data = df.groupby('Country').agg({'Number of new projects': 'sum'}).reset_index()
        top_countries = country_data.nlargest(10, 'Number of new projects')
        fig = px.pie(top_countries, values='Number of new projects', names='Country', title='Các quốc gia hàng đầu theo số dự án')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Country' và 'Number of new projects'")

def plot_pie_chart_top_countries_by_registered_capital(df):
    if 'Country' in df.columns and 'Newly registered capital (million USD)' in df.columns:
        country_data = df.groupby('Country').agg({'Newly registered capital (million USD)': 'sum'}).reset_index()
        top_countries = country_data.nlargest(10, 'Newly registered capital (million USD)')
        fig = px.pie(top_countries, values='Newly registered capital (million USD)', names='Country', title='Các quốc gia hàng đầu theo vốn đăng ký')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Country' và 'Newly registered capital (million USD)'")

def plot_pie_chart_top_countries_by_total_investment(df):
    if 'Country' in df.columns and 'Total investment (million USD)' in df.columns:
        country_data = df.groupby('Country').agg({'Total investment (million USD)': 'sum'}).reset_index()
        top_countries = country_data.nlargest(10, 'Total investment (million USD)')
        fig = px.pie(top_countries, values='Total investment (million USD)', names='Country', title='Các quốc gia hàng đầu theo tổng vốn đầu tư')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Country' và 'Total investment (million USD)'")

def plot_top_10_projects_2022(df):
    if 'Year' in df.columns and 'Country' in df.columns and 'Number of new projects' in df.columns:
        data_2022 = df[df['Year'] == 2022]
        country_data_2022 = data_2022.groupby('Country').agg({'Number of new projects': 'sum'}).reset_index()
        top_10_projects_2022 = country_data_2022.nlargest(10, 'Number of new projects')
        fig = px.bar(top_10_projects_2022, x='Number of new projects', y='Country', orientation='h', title='Top 10 quốc gia theo số dự án năm 2022')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Year', 'Country', và 'Number of new projects'")

def plot_top_10_registered_capital_2022(df):
    if 'Year' in df.columns and 'Country' in df.columns and 'Newly registered capital (million USD)' in df.columns:
        data_2022 = df[df['Year'] == 2022]
        country_data_2022 = data_2022.groupby('Country').agg({'Newly registered capital (million USD)': 'sum'}).reset_index()
        top_10_registered_2022 = country_data_2022.nlargest(10, 'Newly registered capital (million USD)')
        fig = px.bar(top_10_registered_2022, x='Newly registered capital (million USD)', y='Country', orientation='h', title='Top 10 quốc gia theo vốn đăng ký năm 2022')
        st.plotly_chart(fig)
    else:
        st.error("Cần có các cột 'Year', 'Country', và 'Newly registered capital (million USD)'")