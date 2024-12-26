import streamlit as st

st.title("Test Uygulaması")

user_input = st.text_input("Buraya bir şeyler yazın:", "Merhaba!")

if user_input:
    st.write("Yazdığınız:", user_input)
