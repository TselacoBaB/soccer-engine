def normalize(p):
    s=sum(p.values())
    return {k:v/s for k,v in p.items()}

def blend(distributions, weights):
    out={k:0.0 for k in ("home","draw","away")}
    for d,w in zip(distributions,weights):
        for k in out: out[k]+=d[k]*w
    return normalize(out)
