import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
from Academic_Core import AcademicAssistant, AcademicPDFBrain
# Импортируем твой класс (убедись, что файл называется Academic_Core.py)


app = FastAPI()

# Настройка CORS, чтобы браузер не блокировал запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализируем твои классы (не забудь про API ключ в переменных окружения)
assistant = AcademicAssistant()
pdf_brain = AcademicPDFBrain()

@app.post("/chat")
async def chat_endpoint(
    text: str = Form(None), 
    file: UploadFile = File(None)
):
    try:
        # Если пришел файл PDF
        if file and file.filename.endswith('.pdf'):
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            result = pdf_brain.summarize_research(temp_path)
            os.remove(temp_path) # Удаляем временный файл
            return {"reply": result}

        # Если пришел просто текст
        elif text:
            result = assistant.analyze_material(text)
            return {"reply": result}
        
        return {"reply": "Я не получил ни текста, ни PDF файла."}
    
    except Exception as e:
        return {"reply": f"Произошла ошибка на сервере: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)