from soccer_engine.core.engine import DecisionEngine
from soccer_engine.schemas.match import MatchRequest,TeamSnapshot

def test_engine_returns_distribution():
    req=MatchRequest(home=TeamSnapshot(name="A",elo=1600,xg_for=1.8),away=TeamSnapshot(name="B",elo=1450,xg_against=1.5,xg_for=1.0))
    out=DecisionEngine().predict(req)
    assert abs(sum(out["probabilities"].values())-1)<1e-9
    assert out["decision"]["outcome"] in {"home","draw","away"}
