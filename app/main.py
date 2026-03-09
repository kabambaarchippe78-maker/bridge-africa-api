from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()
# CORS pour autoriser Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# modèle des données
class Demande(BaseModel):
    nom: str
    email: str
    telephone: str
    service: str
    pays: str
# route test
@app.get("/")
def home():
    return {"message": "API Bridge Africa fonctionne"}
# route pour recevoir la demande
@app.post("/demandes")
def creer_demande(demande: Demande):
    print(demande)
    return {"message": "Demande reçu"}