import streamlit as st

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="AI Studio v2.8", page_icon="🎨")

# --- 2. SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 3. UI UTAMA ---
st.title("🎨 AI Image Studio v2.8")
st.caption("Mode Stabil: Langsung Muncul Tanpa Ribet")

# Menampilkan Riwayat
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        if chat["type"] == "text":
            st.write(chat["content"])
        else:
            st.image(chat["content"], use_container_width=True)

# --- 4. INPUT & LOGIKA ---
if prompt := st.chat_input("Ketik deskripsi gambar di sini..."):
    # Simpan prompt user
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sedang melukis..."):
            # Membersihkan prompt agar aman untuk URL
            clean_prompt = prompt.replace(" ", "%20")
            
            # Menggunakan Engine Gambar yang paling ringan
            # Kita langsung buat URL-nya
            img_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1080&height=1080&nologo=true&seed=42"
            
            # Langsung tampilkan (Streamlit akan menangani downloadnya secara otomatis)
            try:
                st.image(img_url, caption=f"Hasil: {prompt}", use_container_width=True)
                
                # Simpan ke history
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "type": "image", 
                    "content": img_url
                })
            except:
                st.error("Server sedang sibuk, silakan coba lagi dalam 5 detik.")

# --- 5. FOOTER ---
st.write("---")
st.caption("AI Studio 2026 | Sederhana & Pasti Berhasil")
