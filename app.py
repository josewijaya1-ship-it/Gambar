import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# Load model (sekali saja saat awal)
@st.cache_resource
def load_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32
    )
    pipe = pipe.to("cpu")  # ganti ke "cuda" kalau pakai GPU
    return pipe

pipe = load_model()

# UI Streamlit
st.title("🎨 AI Image Generator")
st.write("Masukkan deskripsi gambar, AI akan membuat gambarnya!")

prompt = st.text_input("Masukkan prompt:", "A futuristic city at sunset")

if st.button("Generate Gambar"):
    with st.spinner("Sedang membuat gambar..."):
        image = pipe(prompt).images[0]
        st.image(image, caption="Hasil AI", use_column_width=True)
