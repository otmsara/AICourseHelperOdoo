import os
from odoo import models, fields
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AICourse(models.Model):
    _name = 'ai.course'
    _description = 'AI Course Helper'

    name = fields.Char(string="Titre du cours", required=True)
    content = fields.Text(string="Contenu du cours")
    summary = fields.Text(string="Résumé généré")
    questions = fields.Text(string="Questions générées")

    def generate_ai_content(self):
        for record in self:
            if not record.content:
                record.summary = "Veuillez saisir le contenu du cours."
                record.questions = ""
                continue

            prompt = f"""
            Voici le contenu d'un cours :

            {record.content}

            1. Fais un résumé clair et structuré.
            2. Génère 5 questions pédagogiques pour les étudiants.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Tu es un assistant pédagogique."},
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content

            # Séparation simple (améliorable plus tard)
            record.summary = result.split("Questions")[0]
            record.questions = result
