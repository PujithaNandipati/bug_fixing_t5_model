import streamlit as st
import torch
from transformers import T5ForConditionalGeneration, RobertaTokenizer

# Load model
MODEL_NAME = "bug_fixing_t5_model"  # Ensure the model is trained & saved here
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

try:
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)
    tokenizer = RobertaTokenizer.from_pretrained(MODEL_NAME)
    st.success("✅ Model loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading model: {e}")

# Function to fix buggy code
def fix_code(buggy_code):
    """Generate a fixed version of the buggy code."""
    input_text = "fix: " + buggy_code
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)
    output_ids = model.generate(input_ids, max_length=512)
    fixed_code = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return fixed_code

# Streamlit UI
st.title("🛠️ Bug Detection & Auto Fixing System")
user_input = st.text_area("🔍 Enter buggy code:")
if st.button("Fix Code"):
    if user_input.strip():
        fixed_output = fix_code(user_input)
        st.subheader("✅ Fixed Code:")
        st.code(fixed_output, language='python')
    else:
        st.warning("⚠️ Please enter some code to fix.")
