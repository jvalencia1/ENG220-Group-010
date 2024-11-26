# -*- coding: utf-8 -*-
"""FINAL_PROJECT_CODE.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RT3ePyhERXRieu12iabaNx2Zgihj31kQ
"""

import pandas as pd
import streamlit as st

# Title of the app
st.title('Gun Violence Data Visualization')

# Preload Data
def read_large_csv(url):
    try:
        chunk_size = 1000
        chunks = pd.read_csv(url, encoding="ISO-8859-1", sep=",", on_bad_lines="skip", chunksize=chunk_size)
        df_list = [chunk for chunk in chunks]
        df = pd.concat(df_list, ignore_index=True)
        return df.dropna()
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Data URL
file_url = "https://raw.githubusercontent.com/BlassMolina03/ENG-220-MATLAB-PROJECTS/main/Data%20Sheet%201.csv"
df = read_large_csv(file_url)

# Data Check
if df is not None:

    # Clean Data
    df['Incident Date'] = pd.to_datetime(df['Incident Date'], errors='coerce')
    df = df.dropna(subset=['Incident Date'])
    df['day_of_week'] = df['Incident Date'].dt.day_name()

    # Show the cleaned data table at the beginning
    st.subheader("Cleaned Data Table")
    st.write(df)

    # Dropdown for graph type selection
    graph_choice = st.selectbox("Choose a graph to view", ["Monthly Increase", "Gender Analysis", "Incidents by City or County", "Incidents by Date"])

    # Process Monthly Analysis
    df['month_year'] = df['Incident Date'].dt.to_period('M')
    monthly_counts = df['month_year'].value_counts().sort_index()

    # Process Gender Analysis
    gender_counts = df['Participant Gender'].value_counts()

    # Process City Or County Analysis
    city_or_county_counts = df['City Or County'].value_counts()  # Correct column name

    # Process Date Analysis
    incident_date_counts = df['Incident Date'].dt.date.value_counts().sort_index()

    if graph_choice == "Monthly Increase":
        st.subheader("Monthly Increase of Gun Violence Incidents")
        st.line_chart(monthly_counts)
        st.write("This chart shows the trend of gun violence incidents per month.")

    elif graph_choice == "Gender Analysis":
        st.subheader("Incidents by Gender")
        st.bar_chart(gender_counts)
        st.write("This chart shows the number of incidents based on participant gender.")

    elif graph_choice == "Incidents by City or County":
        st.subheader("Incidents by City or County")
        st.bar_chart(city_or_county_counts)
        st.write("This chart shows the number of incidents by city or county.")

    elif graph_choice == "Incidents by Date":
        st.subheader("Incidents by Date")
        st.line_chart(incident_date_counts)
        st.write("This chart shows the number of incidents that occurred on each date.")

else:
    st.write("Failed to load data.")