from pymongo import MongoClient

# Connect to MongoDB (You need a MongoDB Atlas account or local setup)
client = MongoClient("mongodb+srv://<your_username>:<your_password>@cluster.mongodb.net/")  
db = client["bug_fixing_db"]
collection = db["bug_fixes"]

def save_to_mongo(buggy_code, fixed_code):
    """Save input and output to MongoDB."""
    collection.insert_one({"buggy_code": buggy_code, "fixed_code": fixed_code, "timestamp": datetime.datetime.utcnow()})
    if model is not None:
    user_input = st.text_area("Enter buggy code:")
    if st.button("Fix Code"):
        inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True)
        output = model.generate(**inputs)
        fixed_code = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Display fixed code
        st.code(fixed_code, language="python")

        # Save to MongoDB
        save_to_mongo(user_input, fixed_code)
