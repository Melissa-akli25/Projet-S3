import streamlit as st
import random
import requests

# Liste temporaire pour stocker les utilisateurs
users = []

# Fonction de météo simulée
def get_weather(city):
    # Exemple de données météo pour Paris
    if city.lower() == 'paris':
        return {'temperature': 18, 'description': 'partiellement nuageux'}
    return None

# Fonction pour recommander des tenues basées sur la température
def recommend_clothes(temperature):
    outfits = []
    if temperature < 10:
        outfits = ["Manteau", "Écharpe", "Gants"]
    elif temperature < 20:
        outfits = ["Pull", "Pantalon", "Chaussures confortables"]
    else:
        outfits = ["T-shirt", "Short", "Chapeau"]
    return outfits

# Accueil
def home():
    st.title("Bienvenue sur l'application Styliste !")
    st.write("Cliquez sur une des options ci-dessous pour commencer.")
    
    page = st.sidebar.radio("Choisissez une page", ["Accueil", "Inscription", "Mot de passe oublié", "Recommandations", "Planification de tenue", "Chatbot"])
    
    if page == "Accueil":
        st.write("Page d'accueil")
        if st.button("S'inscrire"):
            st.experimental_rerun()  # Rediriger vers l'inscription
    
    elif page == "Inscription":
        inscription()

    elif page == "Mot de passe oublié":
        forget_password()

    elif page == "Recommandations":
        recommend_outfits()

    elif page == "Planification de tenue":
        schedule_outfit()

    elif page == "Chatbot":
        chatbot_response()

# Inscription
def inscription():
    st.title("Page d'Inscription")
    username = st.text_input("Nom d'utilisateur")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("S'inscrire"):
        if not username or not email or not password:
            st.error("Tous les champs sont requis")
        else:
            user = {'username': username, 'email': email, 'password': password}
            users.append(user)
            st.success("Utilisateur enregistré avec succès !")
            st.experimental_rerun()  # Rediriger vers la page d'accueil

# Mot de passe oublié
def forget_password():
    st.title("Mot de passe oublié")
    email = st.text_input("Entrez votre email")
    if st.button("Envoyer"):
        st.success(f"Un email a été envoyé à {email} pour réinitialiser votre mot de passe.")

# Recommandations de tenues
def recommend_outfits():
    st.title("Recommandations de tenues")
    city = st.text_input("Entrez votre ville", value='Paris')
    weather_data = get_weather(city)
    
    if not weather_data:
        st.error("Erreur : Ville non trouvée.")
    else:
        temperature = weather_data['temperature']
        description = weather_data['description']
        
        st.write(f"Météo à {city}: {description}, Température: {temperature}°C")
        recommended_outfits = recommend_clothes(temperature)
        st.write("Tenues recommandées:")
        for outfit in recommended_outfits:
            st.write(outfit)

# Planification des tenues
def schedule_outfit():
    st.title("Planification de tenue")
    date = st.date_input("Choisissez une date")
    outfit = st.text_input("Entrez la tenue planifiée")
    
    if st.button("Planifier la tenue"):
        if not outfit:
            st.error("Veuillez entrer une tenue")
        else:
            st.success(f"Tenue planifiée pour le {date}: {outfit}")

# Chatbot
def chatbot_response():
    st.title("Chatbot")
    user_message = st.text_input("Votre message:")
    if st.button("Envoyer"):
        chatbot_reply = "Je suis un chatbot. Comment puis-je vous aider?"
        st.write(f"Réponse du chatbot: {chatbot_reply}")

# Redirection vers des pages externes
def redirect_page():
    if st.button("Rediriger vers dressing"):
        st.experimental_rerun()  # Simuler une redirection

# Fonction principale pour l'application
def main():
    st.set_page_config(page_title="Styliste IA", layout="wide")
    home()  # Appeler la fonction d'accueil

if __name__ == "__main__":
    main()
