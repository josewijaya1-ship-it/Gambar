import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ---
st.set_page_config(page_title="AI Studio v2.5", page_icon="🎨")

# --- 2. SETUP API ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Gunakan Gemini 2.5 Flash
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception as e:
    st.error(f"Setup Gagal: {e}")
    st.stop()

# --- 3. SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- 4. TAMPILAN ---
st.title("🎨 AI Image Studio v2.5")
st.caption("Fokus: Pembuatan Gambar Otomatis")

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        else:
            st.image(msg["content"], use_container_width=True)

# --- 5. LOGIKA ---
if prompt := st.chat_input("Ketik deskripsi gambar..."):
    st.session_state.history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sedang melukis..."):
            try:
                # SETTING SAFETY FILTER KE PALING RENDAH AGAR TIDAK BLOCKED
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]

                # Meminta gambar
                response = model.generate_content(
                    f"Generate a high quality image of: {prompt}",
                    safety_settings=safety_settings
                )
                
                # Cek apakah ada data gambar
                has_image = False
                if response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'inline_data'):
                            img_data = part.inline_data.data
                            st.image(img_data, use_container_width=True)
                            st.session_state.history.append({"role": "assistant", "type": "image", "content": img_data})
                            has_image = True
                            break
                
                if not has_image:
                    # Jika kena filter atau hanya teks
                    text_resp = response.text if response.parts else "Maaf, permintaan ini diblokir oleh filter keamanan Google."
                    st.warning(text_resp)
                    st.session_state.history.append({"role": "assistant", "type": "text", "content": text_resp})

            except Exception as e:
                # Tangani jika finish_reason atau error lainnya muncul
                st.error("Gagal memproses: Coba ganti deskripsi kalimat Anda.")
                st.info("Tips: Gunakan Bahasa Inggris jika Bahasa Indonesia tidak membuahkan hasil.")
