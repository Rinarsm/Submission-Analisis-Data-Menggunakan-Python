import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

# Konfigurasi tampilan
sns.set(style='dark')  
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Judul dashboard
st.title("🚲 Dashboard Analisis Bike Sharing")

# Fungsi untuk memproses DataFrame
def create_yearly_df(df):
    return df.groupby("year").agg({"count": "sum"}).reset_index()

def create_monthly_df(df):
    monthly_df = df.groupby(["month", "year"]).agg({"count": "sum"}).reset_index()
    monthly_df["month"] = pd.Categorical(
        monthly_df["month"],
        categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        ordered=True
    )
    monthly_df = monthly_df.sort_values("month")
    return monthly_df

def create_hourly_df(df):
    return df.groupby(["hour", "year"]).agg({"count": "sum"}).reset_index()

def create_byseason_df(df):
    return df.groupby("season")["count"].sum().reset_index()

# Muat dataset day_df dan hour_df
day_df = pd.read_csv("day_clean.csv")
hour_df = pd.read_csv("hour_clean.csv")

# Konversi kolom tanggal menjadi tipe datetime
day_df["dateday"] = pd.to_datetime(day_df["dateday"])
hour_df["dateday"] = pd.to_datetime(hour_df["dateday"])
min_date = day_df["dateday"].min()
max_date = day_df["dateday"].max()

# Filter data melalui sidebar
with st.sidebar:
    st.image("mountain-bike.jpg")
    start_date, end_date = st.date_input("Rentang Waktu", min_value=min_date, max_value=max_date, value=[min_date, max_date])

filtered_day_df = day_df[(day_df["dateday"] >= pd.Timestamp(start_date)) & (day_df["dateday"] <= pd.Timestamp(end_date))]
filtered_hour_df = hour_df[(hour_df["dateday"] >= pd.Timestamp(start_date)) & (hour_df["dateday"] <= pd.Timestamp(end_date))]

# DataFrame untuk analisis
yearly_df = create_yearly_df(filtered_day_df)
monthly_df = create_monthly_df(filtered_day_df)
season_df = create_byseason_df(filtered_day_df)
season_df["season"] = pd.Categorical(season_df["season"], categories=["spring", "summer", "fall", "winter"], ordered=True)
season_df = season_df.sort_values(by="season")
hourly_df = create_hourly_df(filtered_hour_df)

# Fungsi untuk menambahkan border hitam
def add_black_border(ax):
    for spine in ax.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)

# Visualisasi Penyewaan Sepeda Per Tahun
st.subheader("Performa Penyewaan Sepeda per Tahun")
fig, ax = plt.subplots(figsize=(15, 7))
sns.barplot(x="year", y="count", data=yearly_df, palette=["#a9a9a9", "#2a52be"], ax=ax)

for p in ax.patches:
    ax.text(
        x=p.get_x() + p.get_width() / 2,
        y=p.get_height() + 50,
        s=f'{int(p.get_height()):,}',
        ha="center",
        fontsize=10,
        color="grey"
    )

ax.set_xlabel("Tahun", fontsize=15)
ax.set_ylabel("Jumlah Penyewaan", fontsize=15)
ax.tick_params(axis="x", labelsize=12)
ax.tick_params(axis="y", labelsize=12)
add_black_border(ax)  
st.pyplot(fig)

# Visualisasi Penyewaan Sepeda Per Bulan
st.subheader("Perbandingan Penyewaan Sepeda per Bulan (2011 vs 2012)")
fig, ax = plt.subplots(figsize=(15, 7))
sns.lineplot(x="month", y="count", hue="year", data=monthly_df, marker="o", palette={2011: "red", 2012: "blue"}, ax=ax)

for _, row in monthly_df.iterrows():
    ax.text(
        x=row["month"],
        y=row["count"] - 150,
        s=f'{int(row["count"]):,}',
        color="grey",
        fontsize=10
    )

ax.set_xlabel("Bulan", fontsize=15)
ax.set_ylabel("Jumlah Penyewaan", fontsize=15)
ax.tick_params(axis="x", labelsize=15)
ax.tick_params(axis="y", labelsize=15)
add_black_border(ax)  
st.pyplot(fig)

# Visualisasi Penyewaan Sepeda Per Jam
st.subheader("Jumlah Penyewaan Sepeda per Jam (2011 vs 2012)")
fig, ax = plt.subplots(figsize=(15, 7))
sns.lineplot(x="hour", y="count", hue="year", data=hourly_df, marker="o", palette={2011: "red", 2012: "blue"}, linewidth=1.5, ax=ax)

for _, row in hourly_df.iterrows():
    ax.text(
        x=row["hour"],
        y=row["count"] - 150,
        s=f'{int(row["count"]):,}',
        color="grey",
        fontsize=10
    )

ax.set_xlabel("Jam", fontsize=15)
ax.set_ylabel("Jumlah Penyewaan", fontsize=15)
ax.tick_params(axis="x", labelsize=12)
ax.tick_params(axis="y", labelsize=12)
add_black_border(ax)  
st.pyplot(fig)

# Visualisasi Penyewaan Berdasarkan Musim
st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(15, 7))
sns.barplot(x="season", y="count", data=season_df, palette=["#a9a9a9", "#a9a9a9", "#2a52be", "#a9a9a9"], ax=ax)

for p in ax.patches:
    ax.text(
        x=p.get_x() + p.get_width() / 2,
        y=p.get_height() + 150,
        s=f'{int(p.get_height()):,}',
        ha="center",
        fontsize=10,
        color="grey"
    )

ax.set_xlabel("Musim", fontsize=15)
ax.set_ylabel("Jumlah Penyewaan", fontsize=15)
ax.tick_params(axis="x", labelsize=12)
ax.tick_params(axis="y", labelsize=12)
add_black_border(ax)  
st.pyplot(fig)

# Tambahkan copyright
st.caption("Copyright " + str(datetime.date.today().year) + " " + "[Rina Rismawati](https://www.linkedin.com/in/rinarsm17 'Rina Rismawati | LinkedIn')")
