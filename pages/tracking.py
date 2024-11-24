import streamlit as st
import matplotlib.pyplot as plt
import random
import mysql.connector
from io import BytesIO
from PIL import Image

# Fungsi untuk menghubungkan ke database MySQL
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="facebase"  # Nama database Anda
    )

# Fungsi untuk mengambil data wajah dari database
def get_faces_from_database():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama, hog_features FROM user")  # Ambil data HOG features
    faces = cursor.fetchall()
    conn.close()
    return faces

# Fungsi untuk mensimulasikan data akurasi
def get_accuracy_data():
    return [random.uniform(0.5, 1.0) for _ in range(10)]

# Fungsi untuk memplot grafik akurasi
def plot_accuracy_graph(accuracy_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(1, len(accuracy_data) + 1), accuracy_data, marker='o', color='b', label="Akurasi")
    ax.set_title("Grafik Akurasi Model Pengenalan Wajah")
    ax.set_xlabel("Percakapan")
    ax.set_ylabel("Akurasi")
    ax.legend()
    st.pyplot(fig)

# Fungsi untuk halaman tracking akurasi
def show_tracking_page():
    st.title("Halaman Tracking Akurasi Model")
    st.write("Tracking akurasi model dalam mengenali wajah dan bagaimana algoritma belajar.")
    
    # Data simulasi akurasi
    accuracy_data = get_accuracy_data()
    
    # Plot grafik akurasi
    plot_accuracy_graph(accuracy_data)
    
    st.write("Akurasi model meningkat seiring penggunaan. Jika akurasi rendah, model perlu dilatih lebih lanjut.")
    
    # Ambil wajah yang terdaftar di database
    faces = get_faces_from_database()
    
    if faces:
        st.write("### Wajah yang Terdaftar dalam Database")
        for face in faces:
            user_id, name, hog_features = face
            # Menampilkan ID dan Nama pengguna
            st.write(f"ID: {user_id}, Nama: {name}")
            st.write(f"Fitur HOG (ID: {user_id}) tersedia, namun tidak dapat ditampilkan sebagai gambar.")
    else:
        st.write("Tidak ada wajah terdaftar di database.")

# Fungsi untuk halaman utama (sebagai contoh)
def show_home_page():
    st.title("Halaman Utama")
    st.write("Selamat datang di aplikasi pengenalan wajah.")

# Setup navigasi halaman
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.selectbox("Pilih Halaman", ["Home", "Tracking"], key="page_selectbox")

# Logika pemilihan halaman
if page == "Home":
    st.session_state.page = "Home"
    show_home_page()
elif page == "Tracking":
    st.session_state.page = "Tracking"
    show_tracking_page()
