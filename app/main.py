from dns.e164 import query
from fastapi import Header, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from fastapi import Depends
from fastapi import FastAPI
from app.database import engine, Base
from app.models import Demande
def verifier_token(x_token: str = Header(...)):
    if x_token != "monsecret123":
        raise HTTPException(status_code=401, detail="Token invalide")
app = FastAPI(title="Bridge Africa Travel API")
Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {"message": "API is working"}
class DemandeCreate(BaseModel):
    nom: str
    email: EmailStr
    telephone: str
    pays: str
    service: str
class DemandeResponse(BaseModel):
    id: int
    nom: str
    email: EmailStr
    telephone: str
    pays: str
    service: str
    date_creation: datetime
    statut: str
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/demandes")
def creer_demande(demande: DemandeCreate, db: Session = Depends(get_db)):
    nouvelle_demande = Demande(
        nom=demande.nom,
        email=demande.email,
        telephone=demande.telephone,
        pays=demande.pays,
        service=demande.service,
    )
    db.add(nouvelle_demande)
    db.commit()
    db.refresh(nouvelle_demande)
    return {"message": "Demande enregistrée avec succés"}
@app.get("/demandes", response_model=list[DemandeResponse])
def lire_demandes(pays: str | None, db: Session = Depends(get_db)):
    query = db.query(Demande)
    if pays:
        query = query.filter(Demande.pays == pays)
    demandes = query.all()
    return demandes
@app.delete("/demandes/{demande_id}")
def supprimer_demande(
        demande_id: int,
        db: Session = Depends(get_db),
        token: str = Depends(verifier_token)
):
    demande = db.query(Demande).filter(Demande.id == demande_id).first()
    if not demande:
        return {"message": "Demande non trouvée"}
    db.delete(demande)
    db.commit()
    return {"message": "Demande supprimée avec succès"}
@app.put("/demandes/{demande_id}")
def modifier_demande(demande_id: int, demande: DemandeCreate, db: Session = Depends(get_db)):
    demande_db = db.query(Demande).filter(Demande.id == demande_id).first()
    if not demande_db:
        return {"message": "Demande non trouvée"}
    demande_db.nom = demande.nom
    demande_db.email = demande.email
    demande_db.telephone = demande.telephone
    demande_db.pays = demande.pays
    demande_db.service = demande.service
    db.commit()
    db.refresh(demande_db)
    return {"message": "Demande modifiée avec succès"}