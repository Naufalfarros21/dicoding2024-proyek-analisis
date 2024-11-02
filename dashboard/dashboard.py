import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Analisis Data Bike Sharing", layout="wide")

# Fungsi untuk memuat data
@st.cache_data
def load_data(hour_path, day_path):
    df_hour = pd.read_csv(hour_path)
    df_day = pd.read_csv(day_path)
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    return df_hour, df_day

# Memuat data
hour_path = 'hour.csv'  # Ganti dengan path ke file
day_path = 'day.csv'    # Ganti dengan path ke file
df_hour, df_day = load_data(hour_path, day_path)

# Sidebar untuk pemilihan tampilan
st.sidebar.header("Pengaturan Dashboard")
analysis_option = st.sidebar.selectbox("Pilih Analisis:", ["Per Jam", "Pengaruh Suhu", "Musim", "Akhir Pekan vs Hari Kerja"])

# Menampilkan data frame
st.write("### Tinjauan Data Hour")
st.dataframe(df_hour.head())
st.write("### Tinjauan Data Day")
st.dataframe(df_day.head())

# Visualisasi per jam
if analysis_option == "Per Jam":
    st.subheader("Rata-Rata Penyewaan Sepeda per Jam")
    grouped_hour = df_hour.groupby('hr')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=grouped_hour, x='hr', y='cnt', ax=ax, palette='Blues_d')
    ax.set_title('Rata-Rata Penyewaan Sepeda per Jam dalam Sehari')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-Rata Penyewaan')
    st.pyplot(fig)
    st.markdown("Insight: Diagram ini menunjukkan jam-jam sibuk untuk penyewaan sepeda. Dapat dilihat bahwa terdapat jam-jam tertentu yang memiliki puncak penyewaan lebih tinggi seperti pada jam 8 ketika orang memulai aktivitasnya seperti Sekolah, Bekerja dll. Jam 17 dan 18 ketika orang orang pulang kerja atau sekolah. Berdasarkan data diatas bisa kita gunakan untuk perencanaan operasional dan penjadwalan sumber daya pada jam jam tersebut.")

# Visualisasi pengaruh suhu
elif analysis_option == "Pengaruh Suhu":
    st.subheader("Pengaruh Suhu (Celsius) terhadap Penyewaan Sepeda")
    df_day['temp_celsius'] = df_day['temp'] * 41  # Mengonversi suhu ke Celsius
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df_day, x='temp_celsius', y='cnt', ax=ax, alpha=0.5)
    ax.set_title('Pengaruh Suhu (Celsius) terhadap Penyewaan Sepeda')
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)
    st.markdown("Insight: Scatter plot ini membantu memahami hubungan antara suhu dalam Celsius dan jumlah penyewaan sepeda. Terlihat bahwa suhu yang lebih tinggi atau lebih rendah dapat mempengaruhi jumlah penyewaan, yang penting untuk dipertimbangkan dalam perencanaan musiman.")

# Visualisasi per musim
elif analysis_option == "Musim":
    st.subheader("Penyewaan Sepeda Berdasarkan Musim")
    merged_df = pd.merge(df_hour, df_day[['dteday', 'season']], on='dteday', how='left')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=merged_df, x='season_x', y='cnt', ax=ax)
    ax.set_title('Penyewaan Sepeda Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)
    st.markdown("""
    Keterangan Musim:
    - **Musim Dingin (Winter)**: 1.
    - **Musim Semi (Spring)**: 2.
    - **Musim Panas (Sumer)**: 3.
    - **Musim Gugur (Fall)**: 4.
    """)
    st.markdown("""
    Insight: Boxplot ini menunjukkan bagaimana jumlah penyewaan bervariasi di setiap musim. Penjelasan:
    - **Musim Dingin (Winter)**: Biasanya memiliki jumlah penyewaan terendah karena cuaca yang dingin atau ekstrem.
    - **Musim Semi (Spring)**: Biasanya mengalami peningkatan jumlah penyewaan karena cuaca yang lebih hangat.
    - **Musim Panas (Sumer)**: Seringkali memiliki jumlah penyewaan tertinggi karena cuaca yang optimal untuk aktivitas luar ruangan.
    - **Musim Gugur (Fall)**: Jumlah penyewaan mungkin mulai menurun karena suhu yang mulai mendingin.
    """)
    st.markdown("Kesimpulannya Musim Panas Menjadi Musim yang memiliki lebih banyak penyewaan, selain itu dapat membantu dalam strategi pemasaran dan alokasi sumber daya.")

# Visualisasi akhir pekan vs hari kerja
elif analysis_option == "Akhir Pekan vs Hari Kerja":
    st.subheader("Penyewaan Sepeda: Akhir Pekan vs Hari Kerja")
    df_day['weekday'] = df_day['dteday'].dt.day_name()
    df_day['is_weekend'] = df_day['weekday'].isin(['Saturday', 'Sunday'])
    grouped_weekend = df_day.groupby('is_weekend')['cnt'].mean().reset_index()
    grouped_weekend['type'] = grouped_weekend['is_weekend'].map({True: 'Akhir Pekan', False: 'Hari Kerja'})
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=grouped_weekend, x='type', y='cnt', ax=ax, palette=['#3498db', '#2ecc71'])
    ax.set_title('Rata-Rata Penyewaan Sepeda: Akhir Pekan vs Hari Kerja')
    ax.set_xlabel('Tipe Hari')
    ax.set_ylabel('Rata-Rata Penyewaan')
    st.pyplot(fig)
    st.markdown("Insight: Barplot ini membantu mengidentifikasi perbedaan pola penyewaan antara hari kerja dan akhir pekan. Biasanya, penyewaan pada akhir pekan cenderung lebih tinggi karena waktu luang masyarakat. Tetapi pada Barplot terbalik, jumlah penyewaan pada hari kerja cenderug lebih tinggi.")
    st.markdown("""
    Ini mungkin disebabkan oleh beberapa faktor, yaitu:
    - **Kebutuhan Transportasi Harian**: Orang cenderung menggunakan sepeda untuk bepergian ke tempat kerja atau sekolah selama hari kerja.
    - **Aktivitas Rutin**: Penyewaan sepeda pada hari kerja dapat lebih konsisten karena rutinitas harian.
    - **Pola Penggunaan Berbeda**: Selama akhir pekan, sepeda mungkin lebih sering digunakan untuk rekreasi dan kegiatan santai, yang bisa membuat jumlah total penyewaan lebih rendah dibandingkan dengan penggunaan harian.
    """)

# Footer
st.write("### Kesimpulan")
st.markdown(
    """Analisis ini menunjukkan:
    - Jam-jam sibuk untuk penyewaan sepeda.
    - Hubungan antara suhu dan jumlah penyewaan.
    - Perbedaan penyewaan berdasarkan musim.
    - Perbedaan pola penyewaan antara hari kerja dan akhir pekan.
    """
)
