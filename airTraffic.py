"""
command line usage:
$python airTraffic.py network.dot nodeCaps.txt traffic.dot

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
    print(network.edges())

    removeAntiParallelEdges(network)

    #print (multiEdgeNodes)
    print(network.nodes())
    #print("~~~~~~~~~~~~~~~~~~~")
    print(network.edges())
    #print(nodeCaps)
    #print(traffic)

    file2.close()

def removeAntiParallelEdges(network):
    multiEdgeNodes=[]
    newnodecount =1
    for node1 in network.nodes():
	for node2 in network.nodes():
	    if node1 != node2:
		if(node1 in network.neighbors(node2) and (node2 in network.neighbors(node1))): 
                    if ((node1,node2) not in multiEdgeNodes):
                        multiEdgeNodes.append((node2,node1))
                    #print "~~~~~~~~~~~~~~~~~~~"
		    #print(node1+"->"+node2+" weight: " + str(network[node1][node2][0]['label']))    
				                         		
	    #do anti-parallel edge removal by adding intermediate node

            if ((node1,node2) in multiEdgeNodes):
                #remove edge node1 and node2 
                network.remove_edge(node1,node2)
                #add node newnode 
                newnode = "newnode"+str(newnodecount)
                newnodecount +=1
                network.add_node(newnode)
                #retrieve value for original edge..store in value
                value=network[node2][node1][0]['label'] 
                #add edge from node1 to newnode' ..add value
                network.add_edge(node1, newnode, value) 
                #add edge from newnode to node2.. add value
                network.add_edge(newnode, node2, value)
          


if __name__=="__main__":
    main(sys.argv)
