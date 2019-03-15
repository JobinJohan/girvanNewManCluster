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
    plt.subplot(4, 3, cnt)
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos)


# Implementation of the Girvan-Newman clustering algorithm
def girvanNewmanClustering(graph, nbIteration):
    edges = list(graph.edges)
    fig = plt.figure(figsize=(50,50))
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

    plt.savefig("fig.png")


# ----------------- MAIN ------------------------------------

test = loadData("./data")
# drawGraph(test['Web Mining/Information Fusion'][2])
graph = test['Web Mining/Information Fusion'][2]

# Expected betweenness 24 (see graph on draw.io)
#print(edgesBetweenessCentrality(graph, ('4', '5')))
girvanNewmanClustering(graph, 10)
