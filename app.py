from flask import Flask, request, jsonify, render_template
from calculator.calculator import Calculator
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration de l'API OpenAI
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)

# Initialisation de la classe Calculator
calculator = Calculator()

# Historique des messages
conversation_history = [
    {
        "role": "system",
        "content": "Tu es un assistant qui aide à calculer des pronostics sportifs en utilisant un calculateur alphanumérique. Si l'utilisateur te donne une côte comme '6399 rome', utilise la classe Calculator pour fournir les résultats."
    }
]


def ask_chatgpt(user_input, history):
    """Fonction pour interagir avec l'API ChatGPT"""
    # Ajouter le message de l'utilisateur à l'historique
    history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    # Ajouter la réponse de l'assistant à l'historique
    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})

    return assistant_message


@app.route("/")
def home():
    """Page d'accueil de l'application"""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Endpoint pour gérer les interactions avec ChatGPT"""
    global conversation_history  # Utiliser l'historique global

    user_input = request.json.get("message")

    # Vérifie si l'utilisateur demande un calcul alphanumérique
    if "calcule" in user_input.lower() or "calcul" in user_input.lower():
        # Extrait la côte de l'entrée utilisateur (ex: "6399 rome")
        cote = user_input.split(':')
        results = calculator.perform_task(cote[1].strip())

        if results:
            response = f"Résultats pour {cote[1]} :"
            conversation_history.append({"role": "assistant", "content": results})
            return jsonify({"response": response, "results": results})
        else:
            response = f"Aucun résultat trouvé pour {cote[1]}."
            return jsonify({"response": response})
    else:
        # Si ce n'est pas une demande de calcul, utilise ChatGPT pour répondre
        response = ask_chatgpt(user_input, conversation_history)

    return jsonify({"response": response})


if __name__ == "__main__":
    # run app in debug mode to auto-load our server
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
