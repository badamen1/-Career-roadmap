import openai  
import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv('api_keys.env')  # Ajusta la ruta si es necesario

class Chatbot:
    def __init__(self):
        openai.api_key = os.getenv("openai_apikey")
        self.questions = [
            "¿Cuál es tu nombre?",
            "¿Cuál es tu trabajo actual?",
            "¿Cuál es tu trabajo soñado?",
            "¿Cuáles son tus habilidades actuales? (sepáralas por comas)",
        ]
        self.current_question = 0

    def get_response(self, user_input, chat_history):
        if self.current_question < len(self.questions):
            response = self.questions[self.current_question]
            self.current_question += 1
        else:
            response = self.generate_recommendation(user_input, chat_history)
        return response

    def generate_recommendation(self, user_input, chat_history):
        # Usar todo el historial de chat para el contexto
        chat_context = "\n".join([f"Usuario: {entry['user']}\nAI: {entry['ai']}" for entry in chat_history])
        
        messages = [
            {"role": "system", "content": "Eres un asesor de carrera."},
            {"role": "user", "content": f"Tarea: Proporciona una serie de pasos para ayudar al usuario a alcanzar su trabajo soñado.\nHistoria del chat:\n{chat_context}\n{user_input}"}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Asegúrate de que el modelo sea correcto
                messages=messages
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Ocurrió un error al comunicarse con el chatbot: {str(e)}"

chatbot = Chatbot()