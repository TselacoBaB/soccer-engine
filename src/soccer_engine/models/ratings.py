def elo_win_prob(home_elo: float, away_elo: float, home_advantage: float = 0.0):
    d=(home_elo+home_advantage-away_elo)/400.0
    return 1/(1+10**(-d))

def rating_probs(home_elo: float, away_elo: float, home_advantage: float):
    p=elo_win_prob(home_elo, away_elo, home_advantage)
    return {"home":0.55*p, "draw":0.22, "away":0.55*(1-p)}
