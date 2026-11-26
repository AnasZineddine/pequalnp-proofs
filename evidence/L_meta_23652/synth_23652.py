import sys, json, time
from ortools.sat.python import cp_model
MASK, N, K = 35889, 6, int(sys.argv[1])
pairs=[(i,j) for i in range(N) for j in range(N)]
pins=[set([i]) if i==j else set([i,j]) for (i,j) in pairs]
tgt=[(MASK>>(N*min(i,j)+max(i,j)))&1 for (i,j) in pairs]
print("truthy",sum(tgt),"/",len(tgt),flush=True)
T=len(pairs); NN=N+K
m=cp_model.CpModel(); tab=[[None]*T for _ in range(NN)]
for w in range(N):
    for t in range(T): tab[w][t]=m.NewConstant(1 if w in pins[t] else 0)
for w in range(N,NN):
    for t in range(T): tab[w][t]=m.NewBoolVar(f"w{w}_{t}")
A=[];B=[];OP=[]
for i in range(K):
    a=m.NewIntVar(0,N+i-1,f"a{i}"); b=m.NewIntVar(0,N+i-1,f"b{i}"); op=m.NewIntVar(0,2,f"op{i}")
    m.Add(a<=b); A.append(a);B.append(b);OP.append(op)
    for t in range(T):
        av=m.NewBoolVar("");bv=m.NewBoolVar("")
        m.AddElement(a,[tab[w][t] for w in range(N+i)],av)
        m.AddElement(b,[tab[w][t] for w in range(N+i)],bv)
        c0=m.NewBoolVar("");c1=m.NewBoolVar("")
        m.AddBoolAnd([av,bv]).OnlyEnforceIf(c0); m.AddBoolOr([av.Not(),bv.Not()]).OnlyEnforceIf(c0.Not())
        m.AddBoolOr([av,bv]).OnlyEnforceIf(c1); m.AddBoolAnd([av.Not(),bv.Not()]).OnlyEnforceIf(c1.Not())
        c2=m.NewBoolVar(""); m.AddBoolXOr([c2,av])
        m.AddElement(op,[c0,c1,c2],tab[N+i][t])
for t in range(T): m.Add(tab[NN-1][t]==tgt[t])
s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=120; s.parameters.num_search_workers=8
st=s.Solve(m)
print("status",s.StatusName(st),f"{s.WallTime():.1f}s",flush=True)
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    names=['and','or','not']
    gates=[(s.Value(A[i]),s.Value(B[i]),names[s.Value(OP[i])]) for i in range(K)]
    bad=[]
    for p,want in zip(pins,tgt):
        w=[1 if q in p else 0 for q in range(N)]
        for a,b,op in gates:
            w.append((w[a]&w[b]) if op=='and' else (w[a]|w[b]) if op=='or' else (1-w[a]))
        if w[-1]!=want: bad.append(p)
    print("gates",gates); print("mismatches",len(bad))
    if not bad: json.dump({"gates":gates,"k":K},open("/tmp/sol23652.json","w"))
