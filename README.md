# layout-algorithms
## Some programs realised most common layout CAD algorithms

1. Fiduccia-Mattheyses.py
	
	30/04/22 : Write by @ilyaShafeev on Python 3.8.9 (checked on 3.10.4) and realize, suddenly, Fiduccia-Mattheyses algorithm.

	01/05/22 : Reading config file from command line was added by @vermut42

	Config file example:

		[ca]=2,4,1,4,5 // list of vertices weight
		[bf]=0.375 // balance factor
		[bA]=1,2 // vertices in block A
		[bB]=3,4,5 // vertices in block B
		1,1,1,1,0 // graph incidence matrix
		1,1,0,0,0 // rows - vertices
		0,1,0,0,1 // column - edges
		0,0,1,0,1
		0,0,0,1,0

	Command line: Fiduccia-Mattheyses.py -file var01.txt


BackLog:
 - Graph Constructor (return Adjacency or Incidence matrix with some support information)
 - Basic Clustering Algorithm
 - Codres Algorithm
 - Kernighan – Lin Algorithm
 - Simulated Annealing Algorithm (e.g. find min/max value of function)
 - Genetic Algorithm (e.g. find min/max value of function)
 - Louler's Algorithm
 - h-Metis Algorithm
 - Stockmeyer's Algorithm
 - Force Placement Algorithm
 - Dijkstra's algorithm (with modifications)
 - Lee algorithm (with modifications)
 - Soukup's Algorithm
 - A* Algorithm
 - Mikami‐Tabuchi’s Algorithm
 - Hightower's Algorithm
 - Prim's Algorithm (MST)
 - Kruskal's Algorithm (MST)
 - RMST
 - I1S / BI1S
 - Shallow Light (in progress davidsloun@mail.ru)
 - Kirkpatrick's algorithm
