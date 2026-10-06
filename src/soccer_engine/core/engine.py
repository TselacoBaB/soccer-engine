from soccer_engine.models.poisson import outcome_probs
from soccer_engine.models.ratings import rating_probs
from soccer_engine.core.calibration import blend

class DecisionEngine:
    def _expected_goals(self, req):
        h=req.home; a=req.away; c=req.context
        home=0.65*h.xg_for + 0.35*a.xg_against + c.home_advantage
        away=0.65*a.xg_for + 0.35*h.xg_against
        home*=max(0.75, 1-c.travel_impact)
        away*=max(0.75, 1-c.travel_impact)
        return max(0.05,home), max(0.05,away)

    def predict(self, req):
        hl,al=self._expected_goals(req)
        p_goal=outcome_probs(hl,al)
        p_rating=rating_probs(req.home.elo, req.away.elo, req.context.home_advantage*400)
        wq=max(0.5, req.context.data_quality)
        probs=blend([p_goal,p_rating],[0.65*wq,0.35])
        ranked=sorted(probs.items(), key=lambda x:x[1], reverse=True)
        top,second=ranked[0],ranked[1]
        confidence=max(0,min(1,(top[1]-second[1])*2.2 + 0.55*req.context.data_quality + 0.45*req.context.lineup_certainty - 0.15))
        market={}
        for k,odds in [("home",req.market.home_odds),("draw",req.market.draw_odds),("away",req.market.away_odds)]:
            market[k]={"odds":odds,"implied_probability":None if not odds or odds<=1 else 1/odds,"edge":None if not odds or odds<=1 else probs[k]-1/odds}
        edge_vals=[v["edge"] for v in market.values() if v["edge"] is not None]
        best_edge=max(edge_vals) if edge_vals else None
        score=round(max(0,min(100,confidence*70+(max(0,best_edge) if best_edge is not None else 0)*200+req.context.data_quality*15)))
        if score>=90: action="VERY_STRONG"
        elif score>=80: action="STRONG"
        elif score>=70: action="MODERATE"
        elif score>=60: action="WEAK"
        else: action="NO_ACTION"
        return {"match_id":req.match_id,"probabilities":probs,"expected_goals":{"home":hl,"away":al},"confidence":confidence,"uncertainty":"LOW" if confidence>=0.75 else "MEDIUM" if confidence>=0.5 else "HIGH","market":market,"decision":{"outcome":top[0],"score":score,"classification":action},"drivers":["xG matchup","Elo differential","home advantage","data quality","lineup certainty"]}
