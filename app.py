import streamlit as st
import requests
from urllib.parse import quote

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Image Studio v2.7", page_icon="🎨")

# --- 2. SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- 3. TAMPILAN ---
st.title("🎨 AI Image Studio v2.7")
st.caption("Mode Pasti Berhasil: Menggunakan Engine Gambar Alternatif")

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        else:
            st.image(msg["content"], use_container_width=True)

# --- 4. LOGIKA GENERATE ---
if prompt := st.chat_input("Deskripsikan gambar dalam Bahasa Indonesia..."):
    # Simpan prompt user
    st.session_state.history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sedang melukis untukmu..."):
            try:
                # Kita encode prompt agar aman untuk URL
                encoded_prompt = quote(prompt)
                
                # Kita gunakan Pollinations AI (Sangat stabil & Gratis)
                # Ini akan menghasilkan gambar berkualitas tinggi tanpa filter ribet
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                
                # Verifikasi apakah gambar tersedia
                response = requests.get(image_url)
                
                if response.status_code == 200:
                    st.image(image_url, caption=f"Hasil: {prompt}", use_container_width=True)
                    st.session_state.history.append({"role": "assistant", "type": "image", "content": image_url})
                else:
                    st.error("Gagal mengambil gambar dari server.")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# --- 5. FOOTER ---
st.write("---")
st.caption("Menggunakan AI Engine Terintegrasi (Anti-Block)")
