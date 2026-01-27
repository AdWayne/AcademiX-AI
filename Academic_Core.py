import os
import fitz  # PyMuPDF
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

# Установи свой ключ Groq здесь
os.environ["GROQ_API_KEY"] = "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" 

class AcademicPDFBrain:
    def __init__(self):
        # Используем мощную модель Llama 3.3 через Groq
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.1
        )

    def extract_text_from_pdf(self, file_path):
        text = ""
        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
            return text
        except Exception as e:
            return f"Ошибка при чтении файла: {e}"

    def summarize_research(self, pdf_path):
        raw_text = self.extract_text_from_pdf(pdf_path)
        # У Llama 3.3 большое окно контекста, можем брать больше текста
        context = raw_text[:20000] 

        messages = [
            SystemMessage(content="Ты — научный рецензент. Проанализируй текст и выдели объект, новизну и замечания."),
            HumanMessage(content=f"Текст научной работы:\n{context}")
        ]
        
        response = self.llm.invoke(messages)
        return response.content

class AcademicAssistant:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.2
        )
        
    def analyze_material(self, text_content):
        template = """
        Ты — ведущий научный сотрудник. Проанализируй текст по структуре:
        1. ОСНОВНЫЕ ТЕЗИСЫ.
        2. МЕТОДОЛОГИЧЕСКИЙ АНАЛИЗ.
        3. РЕКОМЕНДУЕМЫЙ СПИСОК ЛИТЕРАТУРЫ.
        
        Текст: {text}
        """
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.llm
        response = chain.invoke({"text": text_content})
        return response.content