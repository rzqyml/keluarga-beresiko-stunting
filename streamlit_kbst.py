import streamlit as st
import pandas as pd

# Membuat DataFrame
df = pd.DataFrame({
    'Nama': ['Alice', 'Bob', 'Charlie'],
    'Usia': [25, 30, 35]
})

# Membuat form input
with st.form(key='my_form'):
    nama_input = st.text_input(label='Masukkan Nama')
    usia_input = st.text_input(label='Masukkan Usia')

    submit_button = st.form_submit_button(label='Submit')

# Menambahkan baris baru ke DataFrame setiap kali tombol "Submit" diklik
if submit_button:
    new_index = len(df) + 1
    new_row = {'Nama': nama_input, 'Usia': int(usia_input)}
    df = df.append(new_row, ignore_index=True)

    # Mengosongkan kolom input setelah tombol "Submit" diklik
    nama_input = ''
    usia_input = ''

# Menampilkan DataFrame
st.write(df)
