# Aim:
The aim of this project is to build a tool to identify communities and influencers in a
academic network. The tool should be able to:
- Load social graph
- Run community detection and centrality methods
- Visualize the network
# Tasks:
## 1- Load the dataset

- Load the Author Network dataset provided in https://aminer.org/lab-datasets/soinf/
The graph consists of authors and coauthor relationships.
## 2- Implementation
- Implement Girvan-Newman clustering algorithm till 10th iteration level.
- Implement Pagerank algorithm.
- Implement Betweenness centrality measure.
Using the previous implementation, perform the following tasks:
- Use Girvan-Newman algorithm to find clusters of authors.
- Find the top-10 authors with highest betweenness centrality.
## 3- Visualization
- Visualize the output of Girvan-Newman algorithm by coloring nodes according to
their assigned groups.
- Visualize the network and highlight the top 10 authors with the highest betweenness
centrality, and top 10 edges with the highest betweenness centrality.
