import rhino3dm as rg
import networkx as nx


def SimpleGraphFromMesh(mesh):

    # Create graph
    G=nx.Graph()

    #Get the full graph
    for i in range(mesh.Faces.Count):
        
        # Add node to graph and get its neighbours
        G.add_node(i)
        neighbours = getAdjancentFaces(mesh ,i)
        
        # Add edges to graph
        for n in neighbours:
            if n > i:
                G.add_edge(i,n)

    return G

def getAdjancentFaces(mesh, MeshFaceIndex):
    sets = []

    for i in range(mesh.Faces.Count):
        sets.append( set(mesh.Faces[i]) )
        
    adj  = []

    for i in range(len(sets)):
        if sets[MeshFaceIndex] is not sets[i]:
            inter = sets[i].intersection(sets[MeshFaceIndex])
            if len(inter) ==2:
                adj.append(i) 

    return adj    

def graphShortestPath(G, source, target):

    return nx.dijkstra_path(G, source, target)

