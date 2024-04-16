import streamlit as st
import pandas as pd
import pickle

# Membaca model
kbst_model = pickle.load(open('kbst_model.sav', 'rb'))

# Judul web
st.title('SISTEM PREDIKSI KELUARGA BERESIKO STUNTING')

# Inisialisasi dataframe kosong
input_result_df = pd.DataFrame()

# Fungsi untuk menambahkan input form dinamis
def add_dynamic_input(num_data):
    data = {}
    for i in range(num_data):
        with st.form(key=f"form_{i}"):
            st.write(f"Data {i+1}")
            data[f"sumber_air_minum_buruk_{i}"] = st.text_input('Apakah Sumber Air Minum Buruk? (1=Ya, 0=Tidak)', '0')
            data[f"terlalu_muda_istri_{i}"] = st.text_input('Apakah Umur Istri Terlalu Muda? (1=Ya, 0=Tidak)', '0')
            data[f"terlalu_dekat_umur_{i}"] = st.text_input('Apakah Umur Suami & Istri Terlalu Dekat? (1=Ya, 0=Tidak)', '0')
            data[f"sanitasi_buruk_{i}"] = st.text_input('Apakah Sanitasi Buruk? (1=Ya, 0=Tidak)', '0')
            data[f"terlalu_tua_istri_{i}"] = st.text_input('Apakah Istri Terlalu Tua? (1=Ya, 0=Tidak)', '0')
            data[f"terlalu_banyak_anak_{i}"] = st.text_input('Apakah Memiliki Banyak Anak? (1=Ya, 0=Tidak)', '0')
            submit_button = st.form_submit_button(label='Tambah Data')
    return data

# Tombol untuk menambah data
num_data = st.number_input("Jumlah data yang ingin diinput", min_value=1, step=1, value=1)
data = add_dynamic_input(num_data)

# Variabel untuk hasil prediksi
kbst_diagnosis = ''

# Tombol untuk prediksi
if st.button('Lakukan Prediksi'):
    for i in range(num_data):
        # Menggunakan model untuk melakukan prediksi
        input_data = {key: int(data[key]) if data[key].isdigit() and int(data[key]) in [0, 1] else None for key in data}

        # Jika ada nilai yang tidak valid, beri tahu pengguna
        if None in input_data.values():
            st.error('Masukkan hanya angka 0 atau 1.')

        else:
            # Membuat DataFrame dari input untuk memudahkan prediksi
            input_df = pd.DataFrame([input_data])

            kbst_prediction = kbst_model.predict(input_df)

            # Menyusun diagnosa berdasarkan hasil prediksi
            kbst_diagnosis = '1' if kbst_prediction[0] == 1 else '0'

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
