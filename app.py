import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'data/BNB-USD.csv'  # Pastikan path file sesuai dengan lokasi file Anda
bnb_data = pd.read_csv(file_path)

# Convert 'Date' column to datetime
bnb_data['Date'] = pd.to_datetime(bnb_data['Date'])

# Set up the page layout
st.set_page_config(layout="wide")

# Tampilkan judul
st.title('Analisis Data BNB-USD')

# Sidebar untuk filter tanggal
st.sidebar.header('Filter Berdasarkan Tanggal')
min_date = bnb_data['Date'].min()
max_date = bnb_data['Date'].max()
start_date, end_date = st.sidebar.slider(
    'Pilih Rentang Tanggal',
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime())
)

# Filter data berdasarkan rentang tanggal
filtered_data = bnb_data[(bnb_data['Date'] >= pd.to_datetime(start_date)) & (bnb_data['Date'] <= pd.to_datetime(end_date))]

# Tampilkan dataframe dalam ukuran kecil di sidebar
st.sidebar.subheader('Dataframe')
st.sidebar.dataframe(bnb_data.head(10))

# Plot Close price
st.subheader('Plot Harga Penutupan (Close)')
fig = px.line(filtered_data, x='Date', y='Close', title='Harga Penutupan BNB-USD')
st.plotly_chart(fig)

# Plot Volume
st.subheader('Plot Volume')
fig = px.line(filtered_data, x='Date', y='Volume', title='Volume Perdagangan BNB-USD', color_discrete_sequence=['orange'])
st.plotly_chart(fig)

# Hitung korelasi
corr = filtered_data[['Close', 'Volume']].corr()

# Plot heatmap korelasi dengan seaborn di bagian bawah
st.subheader('Heatmap Korelasi antara Harga Penutupan dan Volume')
fig, ax = plt.subplots(figsize=(2, 1))  # Mengatur ukuran heatmap
sns.heatmap(corr, annot=True, ax=ax, cmap='coolwarm')
ax.set_title('')
st.pyplot(fig)
