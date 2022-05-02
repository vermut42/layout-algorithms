# layout-algorithms
## Some programs realised most common layout CAD algorithms

1. Fiduccia-Mattheyses.py
	
Write by @ilyaShafeev @ 30/04/22 on Python 3.8.9 (checked on 3.10.4) and realize, suddenly, Fiduccia-Mattheyses algorithm.

Reading config file from command line was added bt vermut42 @ 01/05/22

	Example:

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