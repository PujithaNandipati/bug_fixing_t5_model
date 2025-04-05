# api_server.py
from flask import Flask, request, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

app = Flask(__name__)

# Load model and tokenizer once
model = T5ForConditionalGeneration.from_pretrained("Pujitha633/bug_fixing_t5_model")
tokenizer = T5Tokenizer.from_pretrained("Pujitha633/bug_fixing_t5_model")

@app.route('/fix', methods=['POST'])
def fix_code():
    data = request.get_json()
    code = data.get('code')

    if not code:
        return jsonify({'error': 'Code input is missing.'}), 400

    input_text = f"fix: {code}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=128)
    fixed_code = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return jsonify({
        'fixed_code': fixed_code,
        'bug_type': "unknown"  # you can replace with actual prediction if you have it
    })

if __name__ == '__main__':
    app.run(port=5000)
