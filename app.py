import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Streamlit app setup
st.set_page_config(page_title="Excel Insight Chatbot", layout="wide")
st.title("Excel Insight Chatbot (Powered by OpenRouter LLM)")

# Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel (.xlsx) file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    st.success("File uploaded successfully.")
    st.subheader("Data Preview")
    st.write(df.head())

    question = st.text_input("Enter your question about the data:")

    if question:
        st.write("Processing...")

        # OpenRouter-compatible chat format
        chat_prompt = [
            {
                "role": "system",
                "content": (
                    "You are a helpful data assistant. Generate executable Python pandas code to answer the user's question "
                    "using a dataframe named 'df'. Return the result in a variable named 'result'. "
                    "If a chart is needed, use matplotlib (plt) to plot. "
                    "Do NOT use 'pd.read_csv' or any file reads. Do NOT explain anything. Return only code."
                )
            },
            {
                "role": "user",
                "content": f"My dataframe columns are: {', '.join(df.columns)}.\nQuestion: {question}"
            }
        ]

        def query_openrouter(messages):
            headers = {
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://chatbot.local",  # Use your app URL or GitHub repo if hosting
                "Content-Type": "application/json"
            }

            payload = {
                "model": "mistralai/mistral-7b-instruct",
                "messages": messages,
                "temperature": 0.3
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                raise Exception(f"OpenRouter API error: {response.text}")

        try:
            # Get LLM response and extract Python code
            response_text = query_openrouter(chat_prompt).strip()

            # Clean code block if wrapped in markdown
            if "```python" in response_text:
                code = response_text.split("```python")[1].split("```")[0].strip()
            else:
                code = response_text

            st.subheader("Generated Python Code")
            st.code(code, language="python")

            # Execute the code safely
            local_vars = {"df": df.copy(), "plt": plt}
            exec(code, {}, local_vars)

            # Display result
            if "result" in local_vars:
                result = local_vars["result"]
                if isinstance(result, pd.DataFrame) or isinstance(result, pd.Series):
                    st.subheader("Result")
                    st.write(result)
                elif hasattr(result, "__str__"):
                    st.subheader("Result")
                    st.write(str(result))

            # Display chart if generated
            st.pyplot(plt.gcf())
            plt.clf()

        except Exception as e:
            st.error(f"Error occurred: {e}")
