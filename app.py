import streamlit as st
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from huggingface_hub import login

# Authenticate Hugging Face (only needed if model is private)
HUGGINGFACE_TOKEN = ""  # Replace with your token
login(token=HUGGINGFACE_TOKEN)

# Define the model name
MODEL_NAME = "Pujitha633/bug_fixing_t5_model"  # Ensure this name is correct

@st.cache_resource
def load_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=True)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, use_auth_token=True)
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

st.title("Bug Fixing Model")
st.write("Enter code with bugs, and get a fixed version.")

model, tokenizer = load_model()

if model is not None:
    user_input = st.text_area("Enter buggy code:")
    if st.button("Fix Code"):
        inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True)
        output = model.generate(**inputs)
        fixed_code = tokenizer.decode(output[0], skip_special_tokens=True)
        st.code(fixed_code, language="python")
else:
    st.error("Model could not be loaded. Check authentication and model name.")
