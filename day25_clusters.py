# Cutting three wires will split the network of wires into two clusters.
# Find the product of the sizes of the two clusters.
#
# Researched Louvain algorithm for community detection in graphs
# and deployed it to find clusters of nodes in the network of wires,
# running stages until two super clusters remined ...which had three links between them.


testData = [
'jqt: rhn xhk nvd',
'rsh: frs pzl lsr',
'xhk: hfx',
'cmg: qnr nvd lhk bvb',
'rhn: xhk bvb hfx',
'bvb: xhk hfx',
'pzl: lsr hfx nvd',
'qnr: nvd',
'ntq: jqt hfx bvb xhk',
'nvd: lhk',
'lsr: lhk',
'rzs: qnr cmg lsr rsh',
'frs: qnr lhk lsr',
]


def getConnectionDict(data=testData):
    connectionDict = {}
    for line in data:
        code, connections = line.split(':')
        connectionsList = connections.strip().split(' ')
        if code not in connectionDict.keys():
            connectionDict[code] = []
        connectionDict[code] = connectionDict[code] + connectionsList
        for connection in connectionsList:
            if connection not in connectionDict.keys():
                connectionDict[connection] = []
            connectionDict[connection] = connectionDict[connection] + [code]
    return connectionDict

def getSuperGroups(communities):
    superGroups = {}
    for node in communities.values(): # values are the supergroups
        if node not in superGroups.keys():
            superGroups[node] = node
    for to in communities.keys(): # keys are the nodes belonging to the supergroups
        superGroups[communities[to]].append(to)
    return superGroups

def getM(connectionDict):
    # m is sum weights of all edges within a graph.  
    # Here just the sum of edges
    m = 0
    for node in connectionDict.keys():
        for to in connectionDict[node]:
            m += connectionDict[node][to]
    return m

def getAij(nodeA, nodeB, connectionDict):
    # Aij is the weight of the edge between nodeA and nodeB
    # if there is no edge, Aij is 0
    if nodeB in connectionDict[nodeA]:
        return connectionDict[nodeA][nodeB]
    return 0

def getGroupAij(group, connectionDict):
    # Aij is the sum of all the weigths of edges between connected nodes in the group
    # for a group of a single node, Aij wll be 0
    Aij = 0
    if len(group) == 1: return Aij
    for nodeA in group:
        for nodeB in group:
            if nodeB in connectionDict[nodeA]:
                Aij += getAij(nodeA, nodeB, connectionDict)
    return Aij

def getKi(node, connectionDict):
    # Ki is the sum of link weights of node
    Ki = 0
    for to in connectionDict[node]:
        Ki += connectionDict[node][to]
    return Ki

def getGroupKi(group, connectionDict):
    # Kig is the sum of all link weights of nodes in the group
    Kig = 0
    for node in group:
        Kig += getKi(node, connectionDict)
    return Kig

def getInternalLinks(node, group, connectionDict):
    # KiIn is the sum of all link weights of node i to nodes in the group
    KiIn = 0
    for to in connectionDict[node]:
        if to in group:
            KiIn += connectionDict[node][to]
    return KiIn

def getKroneckerDelta(nodeA, nodeB, group):
    # delta is 1 if nodeA and nodeB are in the same group, 0 otherwise
    if nodeA in group and nodeB in group:
        return 1
    return 0

def withNode(node, group, connectionsDict):
    # delta Q - modularity change if node i is added to group
    # 2m is total link weights in the graph (twice the number of connector 'stubs')
    m = getM(connectionsDict) #toDo lookup once
    ki = getKi(node, connectionsDict) # the number of links (weighted) to node i
    # 2.1 internal link weights, without i
    sumIn = getGroupAij(group, connectionsDict) # sum of weights between nodes in the group
    # 2.2 total link weights, without i Todo lookup
    sumTot = getGroupKi(group, connectionsDict) # sum of all link weights of nodes in the group
    Qbefore = sumIn/(2*m) - (sumTot/(2*m))**2 - (ki/(2*m))**2 # group aand i outside
    # 3. modularity of the community with i
    # 3.1 KiIn, sum of all link weights of node i to nodes in the group
    KiIn = getInternalLinks(node, group, connectionsDict) 
    # 3.2 total link weights, including i
    Qafter = (sumIn + KiIn)/(2*m) - ((sumTot+ki)/(2*m))**2
    return Qafter - Qbefore
  
def withoutNode(node, group, connectionsDict):
    # delta Q - modularity change if node i is removed from group
    # 2m is total link weights in the graph (twice the number of connector 'stubs')
    m = getM(connectionsDict) #toDo lookup once
    ki = getKi(node, connectionsDict) # the number of links (weighted) to node i
    # 2.1 internal link weights, without i
    sumIn = getGroupAij(group, connectionsDict) # toDo lookup once
    # 2.2 total link weights, without i Todo lookup
    sumTot = getGroupKi(group, connectionsDict) # sum of all link weights of nodes in the group
    Qbefore = sumIn/(2*m) - (sumTot/(2*m))**2  # group 
    # 3. modularity of the community with i
    # 3.1 KiIn, sum of all link weights of node i to nodes in the group
    KiIn = getInternalLinks(node, group, connectionsDict) 
    # 3.2 total link weights, including i
    Qafter = (sumIn - KiIn)/(2*m) - (((sumTot-ki)/(2*m))**2 - (ki/(2*m))**2) # group and i outside
    return Qafter - Qbefore

def louvain_algorithm(graph, communitiesCount={}):
    # Initialize each node to its own community
    communities = {node: node for node in graph}
    # initialise count of nodes in each community on first pass
    if len(communitiesCount) == 0:
        communitiesCount = {node: 1 for node in graph}

    if len(communities) == 2:
        return communities, communitiesCount
    
    # First phase: optimize modularity
    while True:
        # Track whether any node has been moved to another community
        moved = False
        
        # Iterate over each node in the graph
        for node in graph:
            # Calculate the modularity change by moving the node to each neighboring community
            best_community = communities[node]
            max_delta_modularity = 0.0
            
            # Get the neighbors of the current node
            neighbors = set(graph[node])

            modularity_lost = withoutNode(node, graph[communities[node]], graph) # modularity lost if node is removed from its current community
            # Calculate the modularity change for each neighboring community
            for neighbor in neighbors:
                neighbor_community = communities[neighbor]
                delta_modularity = withNode(node, graph[neighbor_community], graph) - modularity_lost
                # Check if moving the node to this community improves modularity
                if delta_modularity > max_delta_modularity:
                    max_delta_modularity = delta_modularity
                    best_community = neighbor_community
            
            # Move the node to the community that maximizes modularity improvement
            if best_community != communities[node]:
                communities[node] = best_community
                moved = True
        
        # If no node has been moved, break the loop
        if not moved:
            break
    
    # Second phase: aggregate node communities into super-nodes

    # create a dictionary of super-nodes with lists of node members
    super_nodes = {}
    super_count = {}
    # rename the communities to new super-node names
    communities = {node: 'S_' + community for node, community in communities.items()}
    for node, community in communities.items():
        if community not in super_nodes:
            super_nodes[community] = []
            super_count[community] = 0
        super_nodes[community].append(node)    
        super_count[community] += communitiesCount[node]  # add the count of original, base nodes in each super-node
        
    # create a weighted dictionary of super-nodes, each with a dictionary of other supernodes with weights
    # representing the number of edges between the super-nodes
    super_graph = {super_node: {} for super_node in super_nodes}

    # find other supernodes containing nodes connected to this node
    for super_node in super_nodes:
        for node in super_nodes[super_node]:
            for neighbor in graph[node]:  # graph is the original graph of nodes and connections
                neighbor_community = communities[neighbor]
                if neighbor_community != super_node:
                    if neighbor_community not in super_graph[super_node]:
                        super_graph[super_node][neighbor_community] = 0
                    super_graph[super_node][neighbor_community] += 1
            
    # repeat the first phase with the super-nodes as the nodes in the graph
    communities, communitiesCount = louvain_algorithm(super_graph, super_count)                
  
    return communities, communitiesCount

def solveItPart1(data=testData):
    connections = getConnectionDict(data)
    # add weights to connections - initially 1 for directly connected nodes
    weightedDict = {}
    for fr in connections.keys():
        weightedDict[fr] = {}
        for to in connections[fr]:
            weightedDict[fr][to] = 1
    return louvain_algorithm(weightedDict) #779*778 = 606062

filepath = "day25_input.txt"
with open(filepath, "r") as file:
    data = file.read().splitlines()

print(solveItPart1(data))