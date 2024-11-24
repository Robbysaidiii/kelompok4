import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from HOG import compute_hog_features
from FaceBase import verify_user, register_new_user
from home import show_home

st.title("Aplikasi Pengenalan Wajah Kelompok 4")
st.write("Selamat datang di aplikasi pengenalan wajah! Gunakan menu di sebelah kiri untuk navigasi.")

if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.title("Kelompok 4")
page = st.sidebar.selectbox("Pilih Halaman", ["Home", "Cek Data", "Register"], key="page_selectbox")

if page != st.session_state.page:
    st.session_state.page = page

if st.session_state.page == "Home":
    show_home()

elif st.session_state.page == "Cek Data":
    st.title("Halaman Cek Data")
    st.write("Silakan gunakan webcam Anda untuk melihat data pribadi.")

    upload = st.radio("Pilih metode input gambar:", ("Upload", "Webcam"))

    if upload == "Upload":
        uploaded_image = st.file_uploader("Unggah Gambar", type=['jpg', 'png', 'jpeg'])
        if uploaded_image:
            st.image(uploaded_image, caption="Gambar yang diunggah", use_column_width=True)
            image_bytes = uploaded_image.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            hog_features = compute_hog_features(frame)
            user_info = verify_user(hog_features)
            if user_info != 'unknown_person':
                user_id, name, age, address, college = user_info
                st.success("Wajah dikenali!")
                st.write("**Informasi Pengguna:**")
                st.write(f"**ID:** {user_id}")
                st.write(f"**Nama:** {name}")
                st.write(f"**Umur:** {age}")
                st.write(f"**Alamat:** {address}")
                st.write(f"**Kuliah:** {college}")
            else:
                st.error("Wajah tidak dikenali!")

    elif upload == "Webcam":
        picture = st.camera_input("Gunakan webcam untuk mengambil gambar")
        if picture:
            st.image(picture, caption="Gambar dari webcam", use_column_width=True)
            image_bytes = picture.getvalue()
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            hog_features = compute_hog_features(frame)
            user_info = verify_user(hog_features)
            if user_info != 'unknown_person':
                user_id, name, age, address, college = user_info
                st.success("Wajah dikenali!")
                st.write("**Informasi Pengguna:**")
                st.write(f"**ID:** {user_id}")
                st.write(f"**Nama:** {name}")
                st.write(f"**Umur:** {age}")
                st.write(f"**Alamat:** {address}")
                st.write(f"**Kuliah:** {college}")
            else:
                st.error("Wajah tidak dikenali!")

elif st.session_state.page == "Register":
    st.title("Halaman Register")
    st.write("Silakan isi form untuk mendaftar.")

    user_id = st.text_input("ID Pengguna", key="register_user_id")
    name = st.text_input("Nama", key="register_name")
    age = st.number_input("Umur", min_value=0, key="register_age")
    address = st.text_input("Alamat", key="register_address")
    college = st.text_input("Kuliah", key="register_college")

    enable_camera = st.checkbox("Gunakan kamera untuk mengambil gambar")
    picture = st.camera_input("Ambil gambar untuk registrasi", disabled=not enable_camera)

    if st.button("Daftar"):
        if not (user_id and name and age and address and college):
            st.error("Semua kolom harus diisi!")
        elif not picture:
            st.error("Harap ambil gambar menggunakan kamera!")
        else:
            st.image(picture, caption="Gambar Tangkapan", use_column_width=True)
            image_bytes = picture.getvalue()
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            hog_features = compute_hog_features(frame)
            result = register_new_user(user_id, name, age, address, college, hog_features)
            st.success(result)

