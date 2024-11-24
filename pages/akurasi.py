import streamlit as st
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pandas as pd

# Fungsi untuk menghubungkan ke database MySQL
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="facebase"
    )

# Fungsi untuk mengambil metrik dari database
def get_metrics_from_database():
    """Ambil data metrik dari database, misalnya akurasi, loss, dll."""
    conn = connect_to_database()
    cursor = conn.cursor()

    # Ambil metrik pelatihan dari database
    cursor.execute("SELECT epoch, accuracy, val_accuracy, loss, val_loss FROM training_metrics")
    results = cursor.fetchall()
    
    metrics = {
        "Epoch": [row[0] for row in results],
        "Accuracy": [row[1] for row in results],
        "Validation Accuracy": [row[2] for row in results],
        "Loss": [row[3] for row in results],
        "Validation Loss": [row[4] for row in results],
    }
    
    conn.close()
    return metrics

# Fungsi untuk memplot grafik metrik
def plot_metrics(metrics):
    """Plot training and validation metrics over epochs."""
    epochs = metrics["Epoch"]
    fig, ax = plt.subplots(2, 1, figsize=(12, 10))

    # Plot accuracy
    ax[0].plot(epochs, metrics["Accuracy"], label="Training Accuracy", marker='o', color='b')
    ax[0].plot(epochs, metrics["Validation Accuracy"], label="Validation Accuracy", marker='x', color='orange')
    ax[0].set_title("Training vs Validation Accuracy")
    ax[0].set_xlabel("Epochs")
    ax[0].set_ylabel("Accuracy")
    ax[0].legend()
    ax[0].grid()

    # Plot loss
    ax[1].plot(epochs, metrics["Loss"], label="Training Loss", marker='o', color='g')
    ax[1].plot(epochs, metrics["Validation Loss"], label="Validation Loss", marker='x', color='red')
    ax[1].set_title("Training vs Validation Loss")
    ax[1].set_xlabel("Epochs")
    ax[1].set_ylabel("Loss")
    ax[1].legend()
    ax[1].grid()

    st.pyplot(fig)

# Fungsi untuk menampilkan halaman Tracking
def show_tracking_page():
    """Display the tracking page with accuracy and loss graphs from the database."""
    st.title("Halaman Tracking Akurasi Model")
    st.write("Tracking metrik model: Akurasi dan Loss selama pelatihan.")

    # Ambil data metrik dari database
    metrics = get_metrics_from_database()

    # Plot grafik metrik
    plot_metrics(metrics)

    # Menampilkan tabel metrik
    st.write("### Data Metrik Pelatihan dan Validasi")
    df_metrics = pd.DataFrame(metrics)  # Convert dictionary to DataFrame
    st.dataframe(df_metrics)

# Fungsi untuk menampilkan halaman Home
def show_home():
    st.title("Halaman Utama - Akurasi Pengenalan Wajah Menggunakan model Histogram Of Gradient (HOG)")
    st.write("Selamat datang di aplikasi pengenalan wajah. Di sini, Anda dapat melihat informasi tentang akurasi model, loss, dan tracking pelatihan.")

    # Penjelasan tentang akurasi dan loss
    st.write("### Apa itu Akurasi dan Loss?")
    st.write("""
        - **Akurasi (Accuracy)**: Mengukur seberapa baik model mengenali wajah pada data pelatihan dan validasi. Akurasi tinggi berarti model mengenali wajah dengan baik.
        - **Loss**: Mengukur seberapa jauh prediksi model dari nilai yang sebenarnya. Loss yang rendah berarti model memiliki prediksi yang lebih akurat.
        - **Validation Accuracy dan Validation Loss**: Metrik ini digunakan untuk mengukur performa model pada data yang tidak terlihat sebelumnya, memastikan model tidak menghafal data pelatihan (overfitting).
    """)

    # Ambil data metrik dari database
    metrics = get_metrics_from_database()

    # Plot grafik metrik
    plot_metrics(metrics)

    # Menampilkan tabel metrik
    st.write("### Data Metrik Pelatihan dan Validasi")
    df_metrics = pd.DataFrame(metrics)
    st.dataframe(df_metrics)

    # Penjelasan tentang grafik
    st.write("""
        - **Grafik Akurasi**: Menampilkan akurasi pelatihan dan validasi seiring berjalannya epoch pelatihan. Jika kedua grafik saling mengikuti, itu menunjukkan model belajar dengan baik. 
        - **Grafik Loss**: Menampilkan loss pelatihan dan validasi seiring berjalannya epoch. Loss yang lebih rendah mengindikasikan model semakin baik dalam memprediksi.
    """)

# Fungsi untuk menambahkan metrik ke database
def save_metrics_to_database(epoch, accuracy, val_accuracy, loss, val_loss):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="facebase"
    )
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO training_metrics (epoch, accuracy, val_accuracy, loss, val_loss)
        VALUES (%s, %s, %s, %s, %s)
    """, (epoch, accuracy, val_accuracy, loss, val_loss))

    conn.commit()
    cursor.close()
    conn.close()

# Navigasi
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.title("Navigasi")
page = st.sidebar.selectbox("Pilih Halaman", ["Home"], key="page_selectbox")

# Halaman Logika
if page == "Home":
    show_home()
