import json
from openai import OpenAI
from django.conf import settings

class chatbot():
    def __init__(self):
        api_key = settings.KEYS['openai_apikey']
        self.client = OpenAI(api_key=api_key)
        self.models = {
            'gpt': "gpt-4o-mini",
            'embedding': "text-embedding-3-small"
        }

    def generateRoadmap(self, objective, salary):
        content = f"""Imagina que eres un reclutador experimentado. Se te solicita crear una hoja de ruta de autoestudio de 5 pasos para convertirte en {objective}. Para cada paso de la hoja de ruta, proporciona recomendaciones sobre cómo expandir el tema que estás sugiriendo y algunos materiales que puedes ofrecer. Asegúrate de que cada paso que sugieres esté planeado para aprender algo hacia el objetivo deseado. Concéntrate solo en cursos que pueda hacer desde casa, en línea. Además, proporciona un trabajo al que pueda postularme después de completar cada paso. Justifica cómo esta hoja de ruta me beneficiará en mi carrera profesional y finalmente, después de hacer un análisis, indica si {salary} dólares al año como salario esperado es una buena estimación, o si es demasiado alto o bajo considerando el nivel que se puede alcanzar con esta hoja de ruta.

Proporciona tu respuesta en el siguiente formato JSON:
name: -en lo que quiero convertirme-,
steps: arreglo de pasos en el siguiente formato:
-number: número del paso,
-name: nombre del paso,
-remarkablePoints: arreglo de puntos destacables,
-recommendedMaterials: arreglo de materiales recomendados con el título de cada uno sin URL, y
-jobSuggestion: sugerencia de trabajo como un objeto con: título y descripción.
benefit: Cómo esta hoja de ruta me beneficia.
salary: cadena con tu opinión sobre mis expectativas salariales.
No agregues un punto al final del nombre.
Entrega tu respuesta en el formato de objeto JSON indicado."""
        msg = [
            {"role": "user", "content": content}
        ]
        response = self.client.chat.completions.create(
            model=self.models['gpt'],
            messages=msg,
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        return json.loads(response.choices[0].message.content) # Returns JSON formmated response.

    def embedObjective(self, objective):
        objective = objective.replace("\n", " ")
        return self.client.embeddings.create(input=[objective], model=self.models['embedding']).data[0].embedding
    
 