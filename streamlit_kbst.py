import streamlit as st
import pandas as pd
import pickle

# Load model
kbst_model = pickle.load(open('kbst_model.sav', 'rb'))

# Judul web
st.title('Sistem Prediksi Rekomendasi Beasiswa')

# Kolom isian
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Inisialisasi dataframe kosong
input_data_df = pd.DataFrame(columns=['IPA', 'IPS', 'MTK', 'GEO', 'EKO', 'SOS'])

# Input untuk setiap mata pelajaran
with col1:
    ipa_input = st.text_input('Nilai IPA', value='0')
    input_data_df.loc[0, 'IPA'] = ipa_input

with col2:
    ips_input = st.text_input('Nilai IPS', value='0')
    input_data_df.loc[0, 'IPS'] = ips_input

with col3:
    mtk_input = st.text_input('Nilai MTK', value='0')
    input_data_df.loc[0, 'MTK'] = mtk_input

with col4:
    geo_input = st.text_input('Nilai GEO', value='0')
    input_data_df.loc[0, 'GEO'] = geo_input

with col5:
    eko_input = st.text_input('Nilai EKO', value='0')
    input_data_df.loc[0, 'EKO'] = eko_input

with col6:
    sos_input = st.text_input('Nilai SOS', value='0')
    input_data_df.loc[0, 'SOS'] = sos_input

# Tombol "Tambah Data" untuk menambah index
if st.button('Tambah Data'):
    input_data_df = input_data_df.append(pd.Series(), ignore_index=True)

# Tombol untuk prediksi
if st.button('Lakukan Prediksi'):
    # Menggunakan model untuk melakukan prediksi
    kbst_prediction = kbst_model.predict(input_data_df)

    # Menampilkan hasil prediksi
    if kbst_prediction[0] == 1:
        st.success('Rekomendasi: Diterima untuk Beasiswa')
    else:
        st.error('Rekomendasi: Tidak Diterima untuk Beasiswa')

    # Menambahkan index inputan saat tombol diklik
    input_data_df = input_data_df.append(pd.Series(), ignore_index=True)

# Menampilkan dataframe inputan
st.write('Dataframe Input:')
st.write(input_data_df)
