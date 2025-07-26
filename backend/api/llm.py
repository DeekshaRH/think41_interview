import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"  # Groq-specific

#def ask_groq_llm(messages):
 #   response = openai.ChatCompletion.create(
 #       model="llama3-70b-8192",  # You can use other supported models too
 #       messages=messages,
 #       temperature=0.7
 #   )
  #  return response['choices'][0]['message']['content']

def ask_groq_llm(messages):
    return "Mocked response"

