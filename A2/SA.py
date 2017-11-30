import random



def objective_fun(state):
    for row in state:
        for col in row:
            
    
    
    

    
def generate_neigh(state):
    while True:
        a = random.randint(0,m-1)
        b = random.randint(0,m-1)
        if stage[a][b] == 1:
            break
    while True:
        c = random.randint(0,m-1)
        d = random.randint(0,m-1)
        if stage[a][b] == 0:
            break
    state[a][b], state[c][d] = state[c][d], state[a][b]
    return state

    
def sAnneal(state)
    
    temp = Tmax
    diffState = objective_fun(state)
    if diffState >= eTarget:
        return diffState
    generate_neigh(diffState)
    


def main():
    Tmax=3000.0
    for (m, k) in [(5, 2) , (6, 2), (8, 1), (10, 3)]
        eTarget = k*m*10
        stage = [[0 for x in range(m)] for y in range(m)]]
        while sum(sum(x) for x in stage) > k*m:
            a = random.randint(0,m-1)
            b = random.randint(0,m-1)
            stage[a][b] = 1
        sol = sAnneal(stage)
        viz.visualize(sol)