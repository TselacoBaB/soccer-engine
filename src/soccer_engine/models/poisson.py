import math

def poisson_pmf(k: int, lam: float) -> float:
    return math.exp(-lam) * (lam ** k) / math.factorial(k)

def outcome_probs(home_lambda: float, away_lambda: float, max_goals: int = 8):
    hp=[poisson_pmf(k, home_lambda) for k in range(max_goals+1)]
    ap=[poisson_pmf(k, away_lambda) for k in range(max_goals+1)]
    home=sum(hp[i]*ap[j] for i in range(max_goals+1) for j in range(max_goals+1) if i>j)
    draw=sum(hp[i]*ap[j] for i in range(max_goals+1) for j in range(max_goals+1) if i==j)
    away=sum(hp[i]*ap[j] for i in range(max_goals+1) for j in range(max_goals+1) if i<j)
    s=home+draw+away
    return {"home":home/s,"draw":draw/s,"away":away/s}
