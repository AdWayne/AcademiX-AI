import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyAAIelxmRqm09NEA9twclXpMtl8zJaq89E")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)