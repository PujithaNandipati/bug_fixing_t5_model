from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Replace 'your_hf_username' with your actual Hugging Face username
model_name = "your_hf_username/bug_fixing_t5_model"

# Load the trained model
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Model and tokenizer loaded successfully!")
