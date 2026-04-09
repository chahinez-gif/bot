import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# --- CONFIGURATION ---
load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="CyberBot", page_icon="🤖", layout="centered")

# --- STYLE CYBERPUNK ANIMÉ (CORRIGÉ POUR LA VISIBILITÉ) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@700&display=swap');

/* Fond avec grille animée */
.stApp {
    background-color: #05050f;
    background-image:
        linear-gradient(rgba(180, 79, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(180, 79, 255, 0.05) 1px, transparent 1px);
    background-size: 40px 40px;
    color: #e0e0ff;
    font-family: 'JetBrains Mono', monospace;
}

header[data-testid="stHeader"] { background: transparent; }

/* Animations */
@keyframes glitch {
    0%   { text-shadow: 2px 0 #b44fff, -2px 0 #00d4ff; }
    25%  { text-shadow: -2px 0 #b44fff, 2px 0 #00d4ff; }
    50%  { text-shadow: 2px 2px #b44fff, -2px -2px #00d4ff; }
    75%  { text-shadow: -2px 2px #b44fff, 2px -2px #00d4ff; }
    100% { text-shadow: 2px 0 #b44fff, -2px 0 #00d4ff; }
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes pulse-border {
    0%, 100% { box-shadow: 0 0 8px #b44fff44; }
    50%       { box-shadow: 0 0 22px #b44fffaa, 0 0 40px #b44fff33; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}

/* Titres */
h1 {
    text-align: center;
    font-family: 'Orbitron', monospace !important;
    font-size: 3rem !important;
    background: linear-gradient(90deg, #b44fff, #00d4ff, #b44fff);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glitch 3s infinite;
    letter-spacing: 4px;
    padding: 1.2rem 0 0.3rem 0;
}

.stCaption {
    text-align: center;
    color: #00d4ff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    letter-spacing: 2px;
}

/* --- FIX VISIBILITÉ DES MESSAGES --- */
[data-testid="stChatMessage"] {
    animation: fadeSlideIn 0.35s ease-out;
}

/* Style des bulles Assistant */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, #0a0a1e, #0a1a2e);
    border: 1px solid #00d4ff55;
    border-radius: 16px;
    box-shadow: 0 0 18px #00d4ff22;
}

/* Style des bulles Utilisateur */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #1a0a2e, #2a0a4e);
    border: 1px solid #b44fff66;
    border-radius: 16px;
    animation: pulse-border 3s infinite;
}

/* FORCE LA COULEUR DU TEXTE (IMPORTANT) */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #ffffff !important; /* Blanc pur pour lecture parfaite */
    font-size: 1.05rem !important;
    line-height: 1.6 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Couleur des puces de listes */
[data-testid="stChatMessage"] li::marker {
    color: #00d4ff !important;
    font-weight: bold;
}
/* FORCE LE FOND NOIR PARTOUT SANS MARGE BLANCHE */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMainViewContainer"] {
    background-color: #05050f !important;
}

/* Supprime l'espace vide blanc en bas de la page */
.main .block-container {
    padding-bottom: 0px !important;
}

/* Cache définitivement le footer Streamlit qui peut créer une bande grise/blanche */
footer {
    visibility: hidden;
    height: 0px;
}

/* Assure que la grille va jusqu'au bout */
[data-testid="stAppViewContainer"] {
    background-image:
        linear-gradient(rgba(180, 79, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(180, 79, 255, 0.05) 1px, transparent 1px);
    background-size: 40px 40px;
    background-attachment: fixed;
}
/* Barre de saisie */
[data-testid="stChatInput"] {
    background-color: #05050f !important; /* Couleur identique à .stApp */
    border: 2px solid #b44fff !important; /* Bordure violette néon */
    border-radius: 15px !important;
    padding: 5px !important;
    box-shadow: 0 0 15px rgba(180, 79, 255, 0.2) !important;
}

/* 2. On injecte le robot à l'intérieur à gauche */
[data-testid="stChatInput"]::before {
    content: "🤖";
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.3rem;
    z-index: 10;
    filter: drop-shadow(0 0 5px #00d4ff);
}

/* 3. On paramètre la zone de texte (Transparente + Texte Blanc) */
[data-testid="stChatInput"] textarea {
    background-color:rgba(180, 79, 255, 0.4) !important; /* Pour voir le fond de la barre */
   color: rgba(180, 79, 255, 0.4) !important;             /* Écriture blanche */
    -webkit-text-fill-color: #000000 !important;
    padding-left: 45px !important;           /* Espace pour ne pas écrire sur le robot */
    font-family: 'JetBrains Mono', monospace !important;
    caret-color: #00d4ff !important;         /* Curseur bleu néon */
}

/* 4. On nettoie les résidus gris de Streamlit */
div[data-testid="stChatInput"] > div {
    background-color: transparent !important;
    box-shadow: none !important;
}

/* 5. Optionnel : Placeholder en violet discret */
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(180, 79, 255, 0.4) !important;
}

/* Code blocks */
code {
    background: #1a0a2e !important;
    color: #ff00ff !important; /* Rose néon pour le code */
    padding: 2px 6px !important;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# --- TITRE ---
st.title("🤖 CyberBot")
st.caption(" Assistant IA , Powered by LLaMA ")
st.markdown("<hr style='border: 1px solid #b44fff44; margin: 0.8rem 0 1.2rem 0'>", unsafe_allow_html=True)

# --- INITIALISATION MODÈLE ---
if api_key:
    # Utilisation de Llama 3.1 via Groq
    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=api_key)
else:
    st.error("⚠️ Clé API introuvable ! Vérifie ton fichier .env")
    st.stop()

# --- GESTION MÉMOIRE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Accueil (si aucun message)
if not st.session_state.messages:
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem;'>
        <div style='font-size: 4rem; animation: float 3s infinite;'>⚡</div>
        <h3 style='color: #b44fff;'>Happy To See You</h3>
        <p style='color: #e0e0ff;'>Pose-moi tes questions sur le code ou tes projets.</p>
    </div>
    """, unsafe_allow_html=True)

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ZONE D'INTERACTION ---
if prompt := st.chat_input("Bonjour, comment puis-je vous aider ?..."):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Générer la réponse de l'assistant
    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours..."):
            try:
                # On ajoute une petite consigne système pour forcer les listes propres
                full_prompt = f"Réponds en français. Utilise des listes à puces pour énumérer des idées. \n\nQuestion: {prompt}"

                response = llm.invoke(full_prompt)
                full_response = response.content

                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Erreur système : {e}")
