#  **Taming LLMs with Groq API**  

## Overview  
- This is a chatbot that uses **Groq's API** with the **Llama 3 model** to generate responses. 
- It also has a simple userinterface built with Streamlit.

## What do you need?  
- Python 3.8+ installed  
- Install the required libraries by running:  
  ```
  pip install streamlit groq python-dotenv
  ```

## How to set it up?  
1. **Get your Groq API key** and save it in a `.env` file:  
   ```
   GROQ_API_KEY=your_api_key_here
   ```
2. **Run the chatbot app** by using:  
   ```
   streamlit run LLM.py
   ```

# What’s inside?  
- **LLM.py** → Main chatbot code  
- **.env** → Stores your API key 
- **README.md** → This file  
- **requirements.txt** → List of required libraries  
