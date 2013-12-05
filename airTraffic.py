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

    """  
    network = pgv.AGraph(file1,directed=True)
    traffic = pgv.AGraph(file3, directed=True)
    network = nx.from_agraph(network)
    traffic = nx.from_agraph(traffic)
    """

    network = nx.read_dot(file1) 
    traffic = nx.read_dot(file3)
    
    file2 = open(file2,'r')
    rawNodeCaps = file2.readlines()
    nodeCaps={}
    for line in rawNodeCaps:
        splitLine = line.split()
        nodeCaps[str(splitLine[0])]= int(splitLine[1])

    #while (network.number_of_edges())>(int(network.number_of_nodes())/2):
    backedgeCheck=[]
    for node1 in network:
        for node2 in network:
            if node1 != node2:
                backedgeCheck.append((node1,node2))
                if (node1,node2) and (node2,node1) in backedgeCheck:
                    #do anti-parallel edge removal by adding intermediate node
                    print "there is an anti-parallel edge!"
                    
                else:
                    n = network.number_of_edges(node1, node2)
                    print(n)
                
                
    print backedgeCheck
    #print ("network nodes: " + str(network.nodes()))
    #print "~~~~~~~~~~~~~~"
    #print ("network edges: " +  str(network.edges()))
    #print(nodeCaps)
    #print(traffic)

    
    file2.close()

if __name__=="__main__":
    main(sys.argv)
