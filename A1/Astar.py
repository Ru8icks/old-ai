import assig3, pprint
offsets = (1, 0),(0, 1),(-1, 0),(0,-1)
class SearchNode():
    g = 0 #cost to node
    f = 0 #estimated total cost of a solution path going through this node; f = g + h
    parent = "ROOT"
    kids = []

    def __init__ (self, state, loc):
        self.state = state
        self.loc = loc

    def update(self):
        """function for new f value"""
        self.f = self.g + h(self)
            

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
    """creates a list of states that are the successors to the node, or solution node"""
    succers = []
    x, y = node.loc
    #loops through the offsets for north west etc. try catch for index error if offset causes bad values
    for (ox, oy) in offsets:
        try: 
            if node.state[max(0, x + ox)][max(0, y + oy)] == ".": #checks if node is usable
                new_node = SearchNode(node.state, (x+ox, y+oy))
                new_node = mark(new_node)
                succers.append(new_node) #adds node to successor list named succers
            elif node.state[max(0, x + ox)][max(0, y+ oy)] == "B": #checks if node is solution node
                return node #returns solution node
        except IndexError:
            pass
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
    c.g = p.g + 1
    c.update()
    return c, p

def propagateImprovements(p):
    """function that propagates improvements from parent to children"""
    for c in p.kids:
        if (p.g + 1) < c.g:
            c.parent = p
            c.g = p.g + 1
            c.update()
            propagateImprovements(c)

    
    
def BestFirstSearch(state):
    CLOSED, OPEN = [], [] #lists for open and closed nodes
    node = SearchNode(state, locate(state, 'A'))   #locates start node
    node.g = 0 #sets up intial cost
    node.update() #updates f 
    OPEN.append(node) #adds start node to the list of open nodes for eval
    while True:
        if len(OPEN) == 0: #checks to se if there is an open node
            return "FAILED"
        current = OPEN.pop(0) #gets the first element out of the open list
        CLOSED.append(current) #adds current node to closed list
        moves = successors(current) #gets the children of current node
        if isinstance(moves, SearchNode): #checks if successors() returns solution node
            return"SUCCESS", moves
        for move in moves: 
            current.kids.append(move) #adds children to current move
            if not move in OPEN and not move in CLOSED: #gets hold of moves not in open or closed
                move, current = attachAndEval(move, current) 
                OPEN = _insert(OPEN, move) #organises moves
            
        assig3.visualize(current.state) #draws current state
        
 
if __name__ == "__main__":
    for x in range(1,5):
        with open("board-1-%s.txt"%(x),"r") as f:
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
                tempNode = SearchNode(initialState, node.loc)
                tempNode = mark(tempNode)
                assig3.visualize(tempNode.state)
                node = node.parent