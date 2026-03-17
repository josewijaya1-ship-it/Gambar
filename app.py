import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Studio v2.6 (ID)", page_icon="🎨")

# --- 2. KONFIGURASI API ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Gunakan Gemini 1.5 Pro atau Flash yang stabil
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Setup Gagal: {e}")
    st.stop()

# --- 3. SESSION STATE ---
if "image_history" not in st.session_state:
    st.session_state.image_history = []

# --- 4. UI ---
st.title("🎨 AI Image Studio v2.6")
st.markdown("Buat gambar dengan deskripsi penuh dari imajinasimu.")

# Tampilkan history
for chat in st.session_state.image_history:
    with st.chat_message(chat["role"]):
        if chat["type"] == "text":
            st.write(chat["content"])
        else:
            st.image(chat["content"], use_container_width=True)

# --- 5. LOGIKA GENERATE ---
if prompt := st.chat_input("Deskripsikan gambar Anda dalam Bahasa Indonesia..."):
    # Tampilkan prompt user
    st.session_state.image_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sedang melukis..."):
            try:
                # KONFIGURASI KEAMANAN: SET KE BLOCK_NONE AGAR LEBIH BEBAS
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]

                # MEMINTA GAMBAR DENGAN FILTER KEAMANAN TERENDAH
                response = model.generate_content(
                    f"Generate a very high-quality image based on this specific description: {prompt}",
                    safety_settings=safety_settings
                )

                # Cek apakah ada data gambar
                has_image = False
                if response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'inline_data'):
                            # Menampilkan gambar langsung di Streamlit
                            img_data = part.inline_data.data
                            st.image(img_data, use_container_width=True, caption="Hasil Kreasi AI")
                            st.session_state.image_history.append({"role": "assistant", "type": "image", "content": img_data})
                            has_image = True
                            break

                if not has_image:
                    # Jika AI memberikan respon teks, tampilkan
                    st.write(response.text)
                    st.info("💡 Kadang AI memberikan respon teks. Cobalah deskripsi yang lebih panjang.")
                    st.session_state.image_history.append({"role": "assistant", "type": "text", "content": response.text})

            except Exception as e:
                # Tangani error dengan elegan tanpa menyarankan bahasa Inggris
                st.error("Gagal memproses gambar: Coba ubah deskripsi Anda.")
                st.info("Tips: Berikan instruksi yang lebih detail agar AI lebih mudah memahami konteksnya.")
