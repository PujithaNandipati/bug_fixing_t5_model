import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Connect to SQLite Database (You can switch to PostgreSQL or MongoDB)
conn = sqlite3.connect("bug_metrics.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bug_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bug_type TEXT,
        severity TEXT,
        detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# Streamlit UI
st.title("Bug Detection Dashboard")

# Fetch stored bug metrics
df = pd.read_sql_query("SELECT * FROM bug_metrics", conn)

if not df.empty:
    st.subheader("Bug Metrics Overview")

    # Display DataFrame
    st.dataframe(df)

    # Bug Type Distribution
    st.subheader("Bug Type Distribution")
    fig, ax = plt.subplots()
    df["bug_type"].value_counts().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    # Bug Severity Distribution
    st.subheader("Bug Severity Distribution")
    fig, ax = plt.subplots()
    df["severity"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax)
    st.pyplot(fig)
else:
    st.info("No bug data available. Start testing to populate metrics!")

# Close connection
conn.close()
