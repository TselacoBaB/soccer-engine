from fastapi import FastAPI
from soccer_engine.core.engine import DecisionEngine
from soccer_engine.schemas.match import MatchRequest

app = FastAPI(title="Soccer Decision Engine", version="0.1.0")
engine = DecisionEngine()

@app.get("/health")
def health():
    return {"status":"ok","engine":"soccer-decision-engine"}

@app.post("/v1/decision")
def decision(req: MatchRequest):
    return engine.predict(req)
