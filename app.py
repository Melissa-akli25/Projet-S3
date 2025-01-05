import random
import requests
# Importer Flask
from flask import Flask, request, jsonify, render_template, redirect

# Initialiser l'application Flask
app = Flask(__name__)

# Initialiser l'application Flask et spécifier le dossier de templates personnalisé
app = Flask(__name__)
# Route d'accueil
@app.route('/')
def home():
    return render_template('accueil.html')


# Route pour enregistrer un utilisateur
# Liste pour stocker les utilisateurs (temporaire)
users = []

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    return render_template('inscription/login.html')

# Route pour la page "Mot de passe oublié"
@app.route('/forgotpassword', methods=['GET', 'POST'])
def forget_password():
    return render_template('inscription/forgotpassword.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('inscription/new_compte.html')

    # Récupérer les données envoyées par l'utilisateur
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Vérification si les champs nécessaires sont présents
    if not username or not email or not password:
        return jsonify({'error': 'Tous les champs sont requis'}), 400

    # Ajouter l'utilisateur à la liste
    user = {'username': username, 'email': email, 'password': password}
    users.append(user)

    return jsonify({'message': 'Utilisateur enregistré avec succès !'}), 201



@app.route('/recommend', methods=['GET'])
def recommend_outfits():
    city = request.args.get('city', default='Paris')

    # Récupérer les données météo
    weather_data = get_weather(city)
    if not weather_data:
        return jsonify({'message': 'Erreur: Ville non trouvée.'}), 400

    temperature = weather_data['temperature']
    description = weather_data['description']

    # Connexion à la base de données
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Récupérer tous les vêtements depuis la base
    cursor.execute("SELECT * FROM clothes")
    all_clothes = cursor.fetchall()

    recommended_outfits = []

    # Logique de recommandation basée sur la météo
    if temperature < 10:
        recommended_outfits = [cloth for cloth in all_clothes if 'manteau' in cloth['name'].lower() or 'veste' in cloth['name'].lower()]
    elif temperature < 20:
        recommended_outfits = [cloth for cloth in all_clothes if 'pantalon' in cloth['name'].lower() or 'pull' in cloth['name'].lower()]
    else:
        recommended_outfits = [cloth for cloth in all_clothes if 't-shirt' in cloth['name'].lower() or 'robe' in cloth['name'].lower()]

    # Fermeture de la connexion
    cursor.close()
    connection.close()

    return jsonify({
        'message': 'Voici vos recommandations de tenues !',
        'city': city,
        'weather_description': description,
        'temperature': temperature,
        'recommended_outfits': recommended_outfits
    })

outfits_schedule = []
#route pour plannification 
@app.route('/schedule_outfit', methods=['GET', 'POST'])
def schedule_outfit():
    return render_template('planification/planification.html')
    # Récupérer les données envoyées par l'utilisateur (la tenue et la date)
    data = request.get_json()
    
    # Vérifier que les données nécessaires sont présentes
    if 'date' not in data or 'outfit' not in data:
        return jsonify({"error": "Date et tenue sont requises"}), 400
    
    # Planifier la tenue (ajouter à la liste des tenues planifiées)
    outfit_schedule = {
        "date": data['date'],
        "outfit": data['outfit'],
        "message": "Tenue planifiée avec succès !"
    }
    
    # Ajouter l'élément à la liste
    outfits_schedule.append(outfit_schedule)
    
    # Retourner une réponse
    return jsonify(outfit_schedule), 201
# Exemple de recommandations basées sur l'émotion
outfit_recommendations = {
    "heureux": ["T-shirt coloré", "Jean décontracté", "Chaussures confortables"],
    "triste": ["Veste en laine", "Pantalon sombre", "Chaussettes douillettes"],
    "en_colère": ["Veste en cuir", "Jeans noirs", "Baskets sport"],
    "fatigué": ["Sweat à capuche", "Jogging", "Pantoufles"]
}

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    return render_template('contact/contact.html')
    # Récupérer les données
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Afficher les données dans la console (debug)
    print(f"Nom : {name}, Email : {email}, Message : {message}")

    # Retourner une réponse JSON
    return {"message": "Votre message a bien été envoyé !"}, 200

@app.route('/tendance', methods=['GET', 'POST'])
def tendance():
    return render_template('TENDANCE/Tendance.html')

@app.route('/dressing', methods=['GET', 'POST'])
def dressing():
    return redirect('https://virtualcloser-gbpc7vsxqfwhhgnqy2ysim.streamlit.app')

@app.route('/lookdujour', methods=['GET', 'POST'])
def lookdujour():
    return redirect('https://lookdujour-ajw2y6ppjaic7psm2vgv8n.streamlit.app')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot_response():
    return render_template('CHAT/chat.html')
    user_message = request.json.get('message')  # Message envoyé par l'utilisateur
    # Appeler la fonction de ta collègue qui gère la logique du chatbot
    chatbot_reply = chatbot_logic(user_message)  
    return jsonify({"response": chatbot_reply})
if __name__ == "__main__":
    app.run(debug=True)
    
    


