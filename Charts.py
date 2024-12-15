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

file_path = 'data(fixed).csv'
df = pd.read_csv(file_path, encoding='utf-8')

def charts(df):
    st.title("Biểu đồ thống kê")
    plot_new_projects_by_year(df)
    plot_registered_capital_by_year(df)
    plot_top_countries_by_projects(df)
    plot_top_countries_by_registered_capital(df)
    plot_total_projects_and_investment_by_year(df)
    plot_top_countries_by_total_investment(df)
    plot_pie_chart_top_countries_by_projects(df)
    plot_pie_chart_top_countries_by_registered_capital(df)
    plot_pie_chart_top_countries_by_total_investment(df)
    plot_top_10_projects_2022(df)
    plot_top_10_registered_capital_2022(df)
charts(df)