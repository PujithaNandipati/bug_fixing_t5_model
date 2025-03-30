if model is not None:
    user_input = st.text_area("Enter buggy code:")
    if st.button("Fix Code"):
        inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True)
        output = model.generate(**inputs)
        fixed_code = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Display fixed code
        st.code(fixed_code, language="python")
        
        # Save to database
        save_to_db(user_input, fixed_code)
