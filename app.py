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
        # Vérifie si la côte est bien formatée
        try:
            cote = user_input.split(':')
            if len(cote) < 2:
                raise ValueError("Format de côte invalide. Utilisez 'calcule: <côte>'.")
            cote_value = cote[1].strip()
            results = calculator.perform_task(cote_value)

            if results:
                response = f"Résultats pour {cote_value} :"
                # Convertir les résultats en une chaîne lisible
                results_str = "\n".join([f"{combinaison}: {resultat}" for combinaison, resultat in results])

                # Ajouter les résultats à l'historique comme un message de l'assistant
                conversation_history.append({"role": "assistant", "content": results_str})

                return jsonify({"response": response, "results": results})
            else:
                response = f"Aucun résultat trouvé pour {cote_value}."
                return jsonify({"response": response})
        except ValueError as e:
            return jsonify({"response": str(e)})
        except Exception as e:
            return jsonify({"response": f"Une erreur s'est produite : {str(e)}"})
    else:
        # Si ce n'est pas une demande de calcul, utilise ChatGPT pour répondre
        try:
            response = ask_chatgpt(user_input, conversation_history)
            return jsonify({"response": response})
        except Exception as e:
            return jsonify({"response": f"Une erreur s'est produite lors de la communication avec ChatGPT : {str(e)}"})


if __name__ == "__main__":
    # run app in debug mode to auto-load our server
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
