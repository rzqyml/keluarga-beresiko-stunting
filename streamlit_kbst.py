import streamlit as st
import pandas as pd

# DataFrame awal
df = pd.DataFrame(columns=['Nama', 'Usia'])

# Form input
nama = st.text_input('Masukkan Nama:')
usia = st.number_input('Masukkan Usia:', min_value=0)

# Tombol untuk menambahkan data ke DataFrame
if st.button('Tambah Data'):
    # Menambahkan data ke DataFrame
    df = df.append({'Nama': nama, 'Usia': usia}, ignore_index=True)
    st.success('Data berhasil ditambahkan ke DataFrame.')

# Menampilkan DataFrame
st.write('DataFrame:', df)
