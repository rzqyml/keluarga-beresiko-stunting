import streamlit as st
import pandas as pd
import pickle

# Membaca model
kbst_model = pickle.load(open('kbst_model.sav', 'rb'))

# Judul web
st.title('SISTEM PREDIKSI KELUARGA BERESIKO STUNTING')

# Membuat kolom dengan 3 bagian
col1, col2, col3 = st.columns(3)

# Nilai default untuk setiap input
default_values = {
    'sumber_air_minum_buruk': '0',
    'sanitasi_buruk': '0',
    'terlalu_muda_istri': '0',
    'terlalu_tua_istri': '0',
    'terlalu_dekat_umur': '0',
    'terlalu_banyak_anak': '0'
}

# Inisialisasi dataframe kosong
input_result_df = pd.DataFrame()

# Fungsi untuk input data
def input_data():
    # Input untuk pertanyaan-pertanyaan
    with col1:
        st.session_state.state['sumber_air_minum_buruk'] = st.text_input('Apakah Sumber Air Minum Buruk? (1=Ya, 0=Tidak)', st.session_state.state['sumber_air_minum_buruk'])

    with col2:
        st.session_state.state['terlalu_muda_istri'] = st.text_input('Apakah Umur Istri Terlalu Muda? (1=Ya, 0=Tidak)', st.session_state.state['terlalu_muda_istri'])

    with col3:
        st.session_state.state['terlalu_dekat_umur'] = st.text_input('Apakah Umur Suami & Istri Terlalu Dekat? (1=Ya, 0=Tidak)', st.session_state.state['terlalu_dekat_umur'])

    with col1:
        st.session_state.state['sanitasi_buruk'] = st.text_input('Apakah Sanitasi Buruk? (1=Ya, 0=Tidak)', st.session_state.state['sanitasi_buruk'])

    with col2:
        st.session_state.state['terlalu_tua_istri'] = st.text_input('Apakah Istri Terlalu Tua? (1=Ya, 0=Tidak)', st.session_state.state['terlalu_tua_istri'])

    with col3:
        st.session_state.state['terlalu_banyak_anak'] = st.text_input('Apakah Memiliki Banyak Anak? (1=Ya, 0=Tidak)', st.session_state.state['terlalu_banyak_anak'])

# Tombol untuk input data
if st.button('Mulai Input Data'):
    input_data()

# Variabel untuk hasil prediksi
kbst_diagnosis = ''

# Tombol untuk prediksi
if st.button('Lakukan Prediksi'):
    # Menggunakan model untuk melakukan prediksi
    input_data = {key: int(value) if value.isdigit() and int(value) in [0, 1] else None for key, value in st.session_state.state.items()}

    # Jika ada nilai yang tidak valid, beri tahu pengguna
    if None in input_data.values():
        st.error('Masukkan hanya angka 0 atau 1.')

    else:
        # Membuat DataFrame dari input untuk memudahkan prediksi
        input_df = pd.DataFrame([input_data])

        kbst_prediction = kbst_model.predict(input_df)

        # Menyusun diagnosa berdasarkan hasil prediksi
        if kbst_prediction[0] == 1:
            kbst_diagnosis = '1'
        else:
            kbst_diagnosis = '0'

        # Menambahkan hasil prediksi ke dataframe
        input_df['Hasil Prediksi'] = kbst_diagnosis
        input_result_df = input_result_df.append(input_df, ignore_index=True)

        # Menetapkan nilai default kembali
        st.session_state.state = default_values.copy()

        # Mengatur flag reset menjadi False setelah prediksi
        st.session_state.reset_flag = False

# Menampilkan hasil prediksi
st.success(f'Hasil Prediksi: {kbst_diagnosis}')

# Tombol untuk mengunduh dataframe
if not input_result_df.empty:
    st.write('Dataframe Hasil Prediksi:')
    st.write(input_result_df)
    csv = input_result_df.to_csv(index=False)
    st.download_button('Unduh Dataframe Hasil Prediksi', csv, 'predicted_results.csv')

# Tombol untuk input data lagi
if st.button('Input Data Lagi'):
    input_data()
