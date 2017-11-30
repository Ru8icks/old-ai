import assig3, pprint
offsets = (1, 0),(0, 1),(-1, 0),(0,-1)
COSTTABLE = [100, 50, 10, 5, 1]
class SearchNode():
    g = 0 #cost to node
    f = 0 #estimated total cost of a solution path going through this node; f = g + h
    parent = "ROOT"
    kids = []

    def __init__ (self, state, loc, cost):
        self.state = state
        self.loc = loc
        self.cost = cost

    def update(self):
        """function for new f value"""
        self.f = self.g + h(self) + self.cost
            

def h(node):
    """finds the distance to the goal"""
    Ax, Ay = node.loc
    Bx, By = locate(node.state, 'B')
    return abs(Bx - Ax) + abs(By-Ay)
    
    
def locate (state, char):
    """function for finding a given symbol"""
    for x in range(len(state)):
        for y in range(len(state[0])):
            if state[x][y] == char:
                return (x, y)
                
                
def successors(node):
    """creates a list of states that are the successors to the node, or returns solution node"""
    succers = []
    x, y = node.loc
    #loops through offsets for north, west etc
    for (ox, oy) in offsets:
        try:  
            move = node.state[max(0, x + ox)][max(0, y + oy)]
            if move in "wmfgr":
                cost = COSTTABLE["wmfgr".find(move)] #finds cost of move
                new_node = SearchNode(node.state, (x+ox, y+oy), cost )#creates new node with cost of travel
                new_node = mark(new_node) #marks node as visited  
                succers.append(new_node) #adds node to successor list
            elif node.state[max(0, x + ox)][max(0, y+ oy)] == "B": #checks if node is solution 
                return node #returns solution node
        except IndexError:
            pass #offsets can cause indexError
    return succers
  
def mark(node):
    """" helper function that replaces current location symbol"""
    line = node.state[node.loc[0]]
    line = line[:node.loc[1]] + "Y" + line[node.loc[1]+1:]
    node.state[node.loc[0]] = line
    return node

def _insert(nodes, node):
    """insert a searchnode into a list of searchnodes based on value of searchnode.f (ascending)"""
    if len(nodes) == 0:
        return[node]
    for ax, x in enumerate(nodes):
        if x.f >=node.f:
            nodes.insert(ax, node)
            return nodes
    else: 
        nodes.append(node)
    return nodes
    

def attachAndEval(c, p):
    """attaches child/successor to parent/predecessor and updates values"""
    c.parent = p
    c.g = p.g + p.cost
    c.update()
    return c, p

def propagateImprovements(p):
    """function that propagates improvements from parent to children"""
    for c in p.kids:
        if (p.g + p.cost) < c.g:
            c.parent = p
            c.g = p.g + p.cost
            c.update()
            propagateImprovements(c)

    
    
def BestFirstSearch(state):
    
    CLOSED, OPEN = [], [] #lists for OPEN and CLOSED nodes
    node = SearchNode(state, locate(state, 'A'), 1) #finds start node
    node.g = 0 #sets initial cost
    node.update() #updates f value
    OPEN.append(node) #adds start node to OPEN for eval 

    while True:
        if len(OPEN) == 0: #checks if there exists an OPEN node
            return "FAILED"
        current = OPEN.pop(0)#gets first open node out of open list
        CLOSED.append(current) #adds current node to closed list
        moves = successors(current) #gets current nodes children
        if isinstance(moves, SearchNode): 
            return"SUCCESS", moves #returns success if solution node is returned otherwise list of children are eval
        for move in moves:
            current.kids.append(move) #appends children to current node from moves
            if not move in OPEN and not move in CLOSED: #checks for moves not in open or closed
                move, current = attachAndEval(move, current)
                OPEN = _insert(OPEN, move) #organises moves
            elif current.g + current.cost < move.g: #checks for cheaper path
                move, current = attachAndEval(move, current) #updates relation and cost
                if move in CLOSED:
                    propagateImprovements(move)
             
            
        assig3.visualize(current.state)
        
 
if __name__ == "__main__":
    for x in range(1,5):
        with open("board-2-%s.txt"%(x),"r") as f:
            #double lists representing board
            board = [x.strip("\n") for x in f.readlines()]
            #makes a copy of the init board
            initialState = list(board)
            states = BestFirstSearch(board)
            if states[0] == "SUCCESS":
                node = states[1]
                cost = "Cost from A to B <%s>"%node.f
            #loops through the solution and recreates the shortest path
            while True:
                if node.parent == "ROOT":
                    assig3.visualize(tempNode.state, wait=True, title=cost)
                    break
                tempNode = SearchNode(initialState, node.loc, 1)
                tempNode = mark(tempNode)
                assig3.visualize(tempNode.state)
                node = node.parent