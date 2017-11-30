import assig3, pprint
offsets = (1, 0),(0, 1),(-1, 0),(0,-1)
COSTTABLE = [100, 50, 10, 5, 1, 0, 1]
solution_loc = None

class SearchNode():
    g = 0 #cost to node
    f = 0  #estimated total cost of a solution path going through this node; f = g + h
    parent = "ROOT"
    kids = []
    status = "OPEN"
 

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
    """creates a list of states that are the successors to the node"""
    succers = []
    x, y = node.loc
    #loops through offsets for north, west etc
    for (ox, oy) in offsets: 
        xx, yy = max(0, min(len(node.state)-1, x + ox)), max(0, min(len(node.state[0])-1, y + oy))
        move = node.state[xx][yy]
        if move in "wmfgrB.":
            cost = COSTTABLE["wmfgrB.".find(move)] #finds cost of move
            new_node = SearchNode(node.state, (xx, yy), cost ) #creates new node with cost of travel
            new_node.g = node.g + node.cost #updates new nodes cost to reach from a
            if move != "B": #test to se if not goal
                new_node = mark(new_node)
            new_node.update()    #updates estimated total cost of path
            succers.append(new_node) #appends node to succers list
    return succers
  
def mark(node):
    """" helper function that replaces current location symbol"""
    line = node.state[node.loc[0]]
    line = line[:node.loc[1]] + "Y" + line[node.loc[1]+1:]
    node.state[node.loc[0]] = line
    return node
def dijkstra(nodes, node):
    """insert a searchnode into a list of searchnodes based on dijkstra"""
    if len(nodes) == 0:
        return[node]
    for ax, x in enumerate(nodes):
        if x.g >=node.g:
            nodes.insert(ax, node)
            return nodes
    else: 
        nodes.append(node)
    return nodes

def bfs(nodes, node):
    """insert a searchnode into a list of searchnodes based breath first search"""
    nodes.append(node)
    return nodes
    
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

    
def solution(node):
    """a function that evalueates if given node is solution node"""
    if node.loc == solution_loc:
        return True
    
def BestFirstSearch(state, insert=_insert):
    """main program loop of A. search function that outputs depending on the insert function used, returns solution node """
    global solution_loc
    CLOSED, OPEN = [], [] #creates open and closed lists for sorting nodes
    node = SearchNode(state, locate(state, 'A'), 1) #finds start node
    node.g = 0 #sets initial cost
    node.update() #updates f value
    solution_loc = (locate(state, "B")) #finds solution location
    OPEN.append(node) #adds start node to OPEN list for eval
    while True:
        if len(OPEN) == 0: #checks if there exists OPEN nodes
            return "FAILED"
        current = OPEN.pop(0) #gets first open node out of open list
        CLOSED.append(current) #adds current node to closed list
        current.status = "CLOSED" #closes node
        moves = successors(current) #gets current nodes children
        if solution(current): #checks if current node is solution node, returning current node and open closed lists
            return "SUCCESS", current, OPEN, CLOSED
        for move in moves:
            current.kids.append(move) #appends children to current node from moves
            if not move in OPEN and not move in CLOSED: #checks for moves not in open or closed
                move, current = attachAndEval(move, current)
                OPEN = insert(OPEN, move) #organises moves 
            elif current.g + current.cost < move.g: #checks for cheaper path
                move, current = attachAndEval(move, current)
                if move in CLOSED:
                    propagateImprovements(move)
            
 
if __name__ == "__main__":
    for level in range(1,3):
        for board in range(1,5):
            print level, board
            with open("board-%s-%s.txt"%(level, board),"r") as f:
                #double lists representing board
                board = [x.strip("\n") for x in f.readlines()]
                #makes a copy of the init board
                initialState = list(board)
                searchMode = [_insert, bfs, dijkstra] #list with functions for use
                searchName = ["Astar :", "BFS :", "Dijkstra :"] #name of functions for title
                for name, mode in enumerate(searchMode): #this is probably bad practice but i saw a quick solution (ie use of name)
                    solution_node = BestFirstSearch(list(board), mode) #finds solution node
                    if solution_node[0] == "SUCCESS": #checks if solution is good
                        node = solution_node[1]
                        node.OPEN = solution_node[2]
                        node.CLOSED = solution_node[3]
                        cost = "%s Cost from A to B <%s>"%(searchName[name], node.f)
                        assig3.visualize(node, initialState, title = cost)