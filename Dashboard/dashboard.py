import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

# Konfigurasi tampilan
sns.set(style='dark')  
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Membuat DataFrame
def create_yearly_df(df):
    return df.groupby("year").agg({"count": "sum"}).reset_index()

def create_monthly_df(df):
    return df.groupby(["month", "year"]).agg({"count": "sum"}).reset_index()

def create_hourly_df(df):
    return df.groupby(["hour", "year"]).agg({"count": "sum"}).reset_index()

def create_byseason_df(df):
    return df.groupby(["season", "year"]).agg({"count": "sum"}).reset_index()

# Muat data
all_data = pd.read_csv("./Dashboard/all_df.csv")

# Konversi kolom tanggal
all_data["dateday"] = pd.to_datetime(all_data["dateday"])
min_date = all_data["dateday"].min()
max_date = all_data["dateday"].max()

# Filter data melalui sidebar
with st.sidebar:
    #menambahkan gambar
    st.image ("mountain-bike.jpg")
    start_date, end_date = st.date_input(
        "Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_data = all_data[(all_data["dateday"] >= pd.Timestamp(start_date)) &
                         (all_data["dateday"] <= pd.Timestamp(end_date))]

# DataFrame untuk analisis
yearly_df = create_yearly_df(filtered_data)
monthly_df = create_monthly_df(filtered_data)
hourly_df = create_hourly_df(filtered_data)
season_df = create_byseason_df(filtered_data)

# Tambahkan data tahun 2011 
if 2011 not in yearly_df["year"].values:
    yearly_df = pd.concat([yearly_df, pd.DataFrame({"year": [2011], "count": [0]})], ignore_index=True)
    yearly_df = yearly_df.sort_values(by="year")  

# Judul dashboard
st.title("🚲 Dashboard Analisis Bike Sharing")

# Konfigurasi warna latar belakang dan garis 
plt.rcParams['figure.facecolor'] = 'white'  # Latar belakang utama
plt.rcParams['axes.facecolor'] = '#d3d3d3'  # Latar belakang area grafik
plt.rcParams['axes.edgecolor'] = 'none'    # Mengubah garis sumbu menjadi hitam
plt.rcParams['grid.color'] = 'none'         # Hilangkan grid
plt.rcParams['xtick.color'] = 'black'       # Tick di sumbu x hitam
plt.rcParams['ytick.color'] = 'black'       # Tick di sumbu y hitam

# Menampilkan Statistik Penyewaan Sepeda Per Tahun
st.subheader("Performa Penyewaan Sepeda Per Tahun")
fig, ax = plt.subplots()
sns.barplot(
    data=yearly_df, 
    x="year", 
    y="count", 
    palette=["#808080" if year == 2011 else "#6ca0dc" for year in yearly_df["year"]],  
    ax=ax,
    linewidth=0  
)
plt.xlabel("Tahun")
plt.ylabel("Jumlah Penyewaan")
# Format ulang sumbu y agar tidak menggunakan notasi ilmiah
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
plt.tight_layout()
st.pyplot(fig)

# Statistik Bulanan
st.subheader("Statistik Penyewaan Sepeda Berdasarkan Bulan")
fig, ax = plt.subplots()
sns.lineplot(
    data=monthly_df, 
    x="month", 
    y="count", 
    hue="year", 
    palette={2011: "#808080", 2012: "#6ca0dc"}, 
    marker="o", 
    ax=ax
)
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Statistik Jam
st.subheader("Statistik Penyewaan Sepeda Berdasarkan Jam")
fig, ax = plt.subplots()
sns.lineplot(
    data=hourly_df, 
    x="hour", 
    y="count", 
    hue="year", 
    palette={2011: "#808080", 2012: "#6ca0dc"},  
    marker="o", 
    ax=ax
)
plt.xlabel("Jam")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Statistik Berdasarkan Musim
st.subheader("Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots()
sns.barplot(
    data=season_df, 
    x="season", 
    y="count", 
    hue="year", 
    palette={2011: "#808080", 2012: "#6ca0dc"},  
    ax=ax,
    linewidth=0  
)
plt.ylabel("Jumlah Penyewaan")

# Format bilangan sumbu y tanpa menggunakan notasi ilmiah
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
st.pyplot(fig)

st.caption("Copyright "+ str(datetime.date.today().year) + " " + "[Rina Rismawati](https://www.linkedin.com/in/rinarsm17 'Rina Rismawati | LinkedIn')")
