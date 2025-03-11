import os
import time
from dotenv import load_dotenv
import groq
import streamlit as st

# Class to handle Groq API interactions
class LLMClient:
    def __init__(self, model="llama3-70b-8192"):
        load_dotenv()  # Load API key from .env file
        self.api_key = os.getenv("GROQ_API_KEY")  # Retrieve API key
        self.client = groq.Client(api_key=self.api_key)  # Initialize client
        self.model = model  # Define model

    # Function to generate text completion
    def complete(self, prompt, max_tokens=1000, temperature=0.7):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content  # Return generated text
        except Exception as e:
            print(f"Error: {e}")
            return None

# Function to create structured prompts
def create_structured_prompt(text, question):
    return f"""
    # Analysis Report
    ## Input Text
    {text}
    ## Question
    {question}
    ## Analysis
    """

# Function to extract sections from responses
def extract_section(completion, section_start, section_end="\n"):
    start_idx = completion.find(section_start)
    if start_idx == -1:
        return None
    start_idx += len(section_start)
    end_idx = completion.find(section_end, start_idx)
    if end_idx == -1:
        return completion[start_idx:].strip()
    return completion[start_idx:end_idx].strip()

# Function to classify text with confidence analysis
def classify_with_confidence(client, text, categories, confidence_threshold=0.8):
    prompt = f"""
    Classify the following text into exactly one of these categories: {', '.join(categories)}.
    Response format:
    1. CATEGORY: [one of: {', '.join(categories)}]
    2. CONFIDENCE: [high|medium|low]
    3. REASONING: [explanation]
    Text to classify:
    {text}
    """
    try:
        response = client.complete(prompt)
        category = extract_section(response, "1. CATEGORY: ")
        confidence = extract_section(response, "2. CONFIDENCE: ")
        return {"category": category, "confidence": confidence}
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to calibrate confidence threshold
def calibrate_confidence_threshold(client, test_data, categories):
    total = len(test_data)
    correct = 0
    for text, expected_category in test_data:
        result = classify_with_confidence(client, text, categories)
        if result and result["category"] == expected_category:
            correct += 1
    return correct / total if total > 0 else 0

# Function to compare different models
def compare_models(models, text, categories):
    results = {}
    for model in models:
        client = LLMClient(model)
        results[model] = classify_with_confidence(client, text, categories)
    return results

# Streamlit Web Interface
def main():
    st.title("Content Classification and Analysis Tool")
    text = st.text_area("Enter text to classify:")
    categories = ["Positive", "Negative", "Neutral"]
    if st.button("Classify"):
        client = LLMClient()
        result = classify_with_confidence(client, text, categories)
        st.write(result)

if __name__ == "__main__":
    main()
