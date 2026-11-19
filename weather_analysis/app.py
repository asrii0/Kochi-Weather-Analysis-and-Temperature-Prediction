import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib

st.set_page_config(layout='wide')

#load ML model
model = joblib.load('temp_model.pkl')

# Load weather data

df = pd.read_csv("weather_raw.csv",skiprows=3)
df.columns = ["date","temp_mean","temp_max","temp_min","wind_max","rain"]
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month


# dashboard title

st.title("🌦️ Kochi Weather Dashboard")
st.write("Weather analysis from 2020 to 2025")


# weather summary

st.subheader("Weather Summary")
col1, col2, col3 = st.columns(3)

col1.metric("Average Temperature", f"{df['temp_mean'].mean():.2f} °C")
col2.metric("Average Rainfall", f"{df['rain'].mean():.2f} mm")
col3.metric("Maximum Rainfall", f"{df['rain'].max():.2f} mm")



col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Temperature Over Time")
    fig, ax = plt.subplots(figsize=(5,4))
    ax.plot(df["date"], df["temp_mean"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    st.pyplot(fig)

with col2:
    st.subheader("Yearly Rainfall")
    yearly_rain = df.groupby("year")["rain"].sum()
    fig, ax = plt.subplots(figsize=(5,4))
    ax.bar(yearly_rain.index, yearly_rain.values)
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Rainfall (mm)")
    st.pyplot(fig)

with col3:
    st.subheader("Average Rainfall by Month")
    monthly_rain = df.groupby("month")["rain"].mean()
    fig, ax = plt.subplots(figsize=(5,4))
    ax.bar(monthly_rain.index, monthly_rain.values)
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Rainfall (mm)")
    st.pyplot(fig)



# TEMPERATURE PREDICTION

st.divider()
st.subheader("🌡️ Temperature Prediction")

temp_max = st.number_input("Maximum Temperature")
temp_min = st.number_input("Minimum Temperature")
wind_max = st.number_input("Maximum Wind Speed")
rain = st.number_input("Rainfall")

if st.button("Predict Temperature"):
    prediction = model.predict([[temp_max, temp_min, wind_max, rain]])

    st.success(
        f"Predicted Average Temperature: {prediction[0]:.2f} °C"
    )