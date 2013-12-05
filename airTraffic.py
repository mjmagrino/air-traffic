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


    print(network.nodes())
    print("~~~~~~~~~~~~~~")
    print(network.edges())
    #print(nodeCaps)
    #print(traffic)

    
    file2.close()

if __name__=="__main__":
    main(sys.argv)
