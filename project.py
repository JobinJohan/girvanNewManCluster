import networkx as nx
from pprint import pprint
import operator
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import math

def loadData(directoryPath):
    files = os.listdir(directoryPath)
    # dictionary wrt to the following format: {topic1:[[network1],[network2]]}
    allGraphsOfEachTopic = {}
    for file in files:
        topic = ""
        if "T16" in file:
            topic = "Data Mining/Association Rules"
        elif "T107" in file:
            topic = "Web Services"
        elif "T131" in file:
            topic = "Bayesian Networks/Belief function"
        elif "T144" in file:
            topic = "Web Mining/Information Fusion"
        elif "T145" in file:
            topic = "Semantic Web/Description Logics"
        elif "T162" in file:
            topic = "Machine Learning"
        elif "T24" in file:
            topic = "Database Systems/XML Data"
        elif "T75" in file:
            topic = "Information Retrieval"
        else:
            topic = "Unknown"

        graphToBuild = nx.Graph()
        graphToBuild.name = topic.replace('/', ' ').replace(' ', '')

        # constant
        VERTEX = 0
        EDGE = 1
        TRIANGLE = 2

        f = open("./data/" + file)

        # Vertices: Int "String" Int -> NodeID, personName, #papers
        # Edges: Int Int Int -> sourceNodeID, DestNodeID, #coauthoredPapers
        # Triangles: Int,Int,Int,Int -> NodeID1, NodeID2, NodeID3, #coauthoredPapers
        for line in f:
            if "*Vertices" in line:
                typeOfLine = VERTEX
            elif "*Edges" in line:
                typeOfLine = EDGE
            elif "*Triangles" in line:
                typeOfLine = TRIANGLE
            else:
                if typeOfLine == VERTEX:
                    graph_edge_list = [s.replace(' ','') for s in re.split('"', line)]
                    graphToBuild.add_node(graph_edge_list[0], name=graph_edge_list[1], nbpapers=graph_edge_list[2])
                elif typeOfLine == EDGE:
                    graph_edge_list = line.split()
                    graphToBuild.add_edge(graph_edge_list[0], graph_edge_list[1], coauthoredPapers=graph_edge_list[2])
                elif typeOfLine == TRIANGLE:
                    graph_edge_list = line.split(',')
                    graphToBuild.add_edge(graph_edge_list[0], graph_edge_list[1], coauthoredPapersTriangle=graph_edge_list[3])
                    graphToBuild.add_edge(graph_edge_list[0], graph_edge_list[2], coauthoredPapersTriangle=graph_edge_list[3])
                    graphToBuild.add_edge(graph_edge_list[1], graph_edge_list[2], coauthoredPapersTriangle=graph_edge_list[3])

        if topic in allGraphsOfEachTopic:
            allGraphsOfEachTopic[topic].append(graphToBuild)
        else:
            allGraphsOfEachTopic[topic] = [graphToBuild]

    return allGraphsOfEachTopic

# Compute the betweenness centrality of a given node: not used in this project
def nodesBetweennessCentrality(graph, node):
    centrality = 0
    nodes = list(graph.nodes())

    for vi in range(len(nodes)-1):
        for vj in range(vi+1, len(nodes)):
            if(nodes[vi] == node or nodes[vj] == node):
                continue

            shortestPaths = list(nx.all_shortest_paths(graph, source=nodes[vi], target=nodes[vj]))
            nbPathsIncludingNode = sum(path.count(node) for path in shortestPaths)
            centrality += nbPathsIncludingNode / len(shortestPaths)
    return centrality




# Function that computes the betweenness centrality of a given edge
def edgesBetweenessCentrality(graph, edge):
    centrality = 0
    nodes = list(graph.nodes())

    for vi in range(len(nodes) - 1):
        for vj in range(vi + 1, len(nodes)):
            try:
                shortestPaths = list(nx.all_shortest_paths(graph, source=nodes[vi], target=nodes[vj]))
                nbPathsIncludingEdge = sum(edgeIsInPath([edge[0], edge[1]], path) for path in shortestPaths)
                centrality += nbPathsIncludingEdge / len(shortestPaths)
            except nx.NetworkXNoPath:
                continue
    return centrality


# Function that checks if an edge is contained in a path of an undirected graph (the path is a list of nodes)
def edgeIsInPath(edge, path):
    pathReversed = list(reversed(path))
    n = len(edge)

    if edge in (path[i:i + n] for i in range(len(path) + 1 - n)) or edge in (pathReversed[j:j + n] for j in range(len(pathReversed) + 1 - n)):
        return 1
    else:
        return 0

# Function that draws the given graph and displays the labels of each edge
def drawGraph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos)
    plt.show()

def drawGraphs(G, cnt):
    test = plt.subplot(4, 3, cnt)
    if (cnt == 1):
        test.title.set_text('Initial state of the graph')
    else:
        test.title.set_text('State of the graph at iteration: {}, number of communities: {}'.format(cnt-1, nx.number_connected_components(G)))
    test.set_yticklabels([])
    test.set_xticklabels([])
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos)
    nx.draw_networkx_edge_labels(G, pos)

# draws a graph where communities are drawn using different colors
def drawColoredGraph(G):
    test = plt.subplot(4,3,12)
    test.set_yticklabels([])
    test.set_xticklabels([])
    test.title.set_text('Resulting communities ({})'.format(nx.number_connected_components(G)))
    pos = nx.spring_layout(G)
    colors = ['red', 'green', 'orange', 'cyan', 'magenta', 'yellow', 'pink', 'white', 'brown', 'wheat']
    connected_components = nx.connected_component_subgraphs(G)
    for index, sg in enumerate(connected_components):
        nx.draw_networkx(sg, pos = pos, edge_color = colors[index], node_color = colors[index])


# Implementation of the Girvan-Newman clustering algorithm
def girvanNewmanClustering(graph, nbIteration):
    edges = list(graph.edges)
    fig = plt.figure(figsize=(50, 50))
    drawGraphs(graph, 1)
    cnt = 2

    if len(edges) == 0:
        return "Empty graph"

    while(len(list(graph.edges)) > 0 and nbIteration > 0):
        nbIteration = nbIteration - 1
        highestEdge = ""
        highestScore = -float('inf')
        for edge in edges:
            score = edgesBetweenessCentrality(graph, edge)
            if score > highestScore:
                highestScore = score
                highestEdge = edge

        graph.remove_edge(highestEdge[0], highestEdge[1])
        drawGraphs(graph, cnt)
        cnt += 1

    drawColoredGraph(graph)

    plt.savefig("./Figures/GirvanNewman/{}.png".format(graph.name))


def pageRankCentrality(graph, alpha, beta):
    # Transposition of matrix
    adjacencyMatrix = nx.to_numpy_matrix(graph, weight='None')
    amTransposed = np.transpose(adjacencyMatrix)

    # Diagonal Matrix
    diagonalMatrix = np.zeros([adjacencyMatrix.shape[0], adjacencyMatrix.shape[1]])
    row, col = np.diag_indices(diagonalMatrix.shape[0])
    # Compute the values that have to be filled into the diagonal
    diagonalMatrix[row, col] = [1 / degree[1] for degree in list(graph.degree())]

    # Identity matrix
    identityMatrix = np.identity(adjacencyMatrix.shape[0])

    # Vector of ones
    ones = np.ones((adjacencyMatrix.shape[0], 1))
    pageRankCentrality = np.dot(beta * np.linalg.inv((identityMatrix - np.dot(alpha * amTransposed, diagonalMatrix))), ones)

    return pageRankCentrality


# ----------------- MAIN ------------------------------------
# create output directories
if not os.path.exists('./Figures/GirvanNewman'):
    os.makedirs('./Figures/GirvanNewman')


test = loadData("./data")
# # drawGraph(test['Web Mining/Information Fusion'][2])
# graph = test['Web Mining/Information Fusion'][2]
graph = test['Semantic Web/Description Logics'][1]
# graph2 = graph.copy()
# Expected betweenness 24 (see graph on draw.io)
#print(edgesBetweenessCentrality(graph, ('4', '5')))
# graph = nx.Graph();
# graph.add_nodes_from([1,2,3,4,5])
# graph.add_edges_from([(1,2),(1,4),(1,5),(2,3),(2,5),(3,4),(3,5)])
# graph = nx.read_edgelist('pagerank.txt', nodetype=int)
girvanNewmanClustering(graph, 10)
# print(pageRankCentrality(graph, 0.95, 0.1))
