"""
Makes use of:
    pygraphviz -> http://pygraphviz.github.io/documentation/latest/reference/agraph.html
    networkx -> http://networkx.lanl.gov/reference/drawing.html    
"""

import networkx as nx
import pygraphviz as pgv
import sys


def main(argv):
    
    file1 = argv[1]
    file2 = argv[2]
    file3 = argv[3]

    network = nx.read_dot(file1) 
    traffic = nx.read_dot(file3)
    
    file2 = open(file2,'r')
    rawNodeCaps = file2.readlines()
    nodeCaps={}
    for line in rawNodeCaps:
        splitLine = line.split()
        nodeCaps[str(splitLine[0])]= int(splitLine[1])

    #while (network.number_of_edges())>(int(network.number_of_nodes())/2):

    for node1 in network:
	for node2 in network:
	    if node1 != node2:
	    
		if(node1 in network.neighbors(node2) and (node2 in network.neighbors(node1))): 
		
		    print "~~~~~~~~~~~~~~~~~~~"
		    print(node1+"->"+node2+" weight: " + str(network[node1][node2][0]['label']))    
		
		elif (node2 in network.neighbors(node1)and (node1 in network.neighbors(node2))):
	
		    print "~~~~~~~~~~~~~~~~~~~"
		    print(node2+"->"+node1+" weight: " + str(network[node2][node1][0]['label']))

		else:
		    n = network.number_of_edges(node1, node2)
		    #print(n)              
		     
		
	    #do anti-parallel edge removal by adding intermediate node
    
    #print(network.nodes())
    print("~~~~~~~~~~~~~~~~~~~")
    #print(network.edges())

    #print(network)
    #print(nodeCaps)
    #print(traffic)

    
    file2.close()

if __name__=="__main__":
    main(sys.argv)
