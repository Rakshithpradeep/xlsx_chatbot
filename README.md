# Excel Insight Chatbot

A conversational assistant that enables users to gain insights from Excel (`.xlsx`) files using natural language. Powered by OpenRouter's LLM (Mistral 7B), the chatbot interprets questions and returns responses as Python-generated text, tables, or charts.

## Features

- Upload `.xlsx` files (up to ~500 rows)
- Ask natural language questions like:
  - "What is the average salary?"
  - "Show a bar chart of employees by department"
- Automatically:
  - Parses and normalizes data
  - Detects intent (summary, filter, chart)
  - Generates Pandas + Matplotlib code using an LLM
- Schema-agnostic: No hardcoded column names

## Create virtual environment & install dependencies:
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt
## to Run the app:
streamlit run app.py

