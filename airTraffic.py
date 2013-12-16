"""
command line usage:
$python airTraffic.py network.dot nodeCaps.txt traffic.dot

Makes use of:
    pygraphviz -> http://pygraphviz.github.io/documentation/latest/reference/agraph.html
    networkx -> http://networkx.lanl.gov/reference/drawing.html    
"""

import networkx as nx
import pygraphviz as pgv
from matplotlib import pylab as plt
import sys


def main(argv):
    
    file1 = argv[1]
    file2 = argv[2]
    file3 = argv[3]

    network = nx.read_dot(file1)

    #print(network)
    
    
    file2 = open(file2,'r')
    rawNodeCaps = file2.readlines()
    nodeCaps={}
    for line in rawNodeCaps:
        splitLine = line.split()
        nodeCaps[str(splitLine[0])]= int(splitLine[1])

    airTrafficGraph = nx.DiGraph()
    airTrafficGraph = nx.DiGraph(name='AirTraffic')
    airTrafficGraph.add_nodes_from(network)

    edgelist = []
    edgetuples = network.edges()
    
    for edgetuple in edgetuples:
        tmplist =[]
        tmplist.append(edgetuple[0])
        tmplist.append(edgetuple[1])
        edgelist.append(tmplist)

    for edge in edgelist:
        edge.append({"capacity":int(network[edge[0]][edge[1]][0]['label'])})
        #edge.append({"label":int(network[edge[0]][edge[1]][0]['label'])})
    airTrafficGraph.add_edges_from(edgelist)
    
   
##    print(network.edges())

   
    #print(airgraph.edges())
   


    traffic = nx.read_dot(file3)
    #print(traffic)
    airTrafficGraph.add_nodes_from(traffic)

    edgelist = []
    edgetuples = traffic.edges()
    
    for edgetuple in edgetuples:
        tmplist =[]
        tmplist.append(edgetuple[0])
        tmplist.append(edgetuple[1])
        edgelist.append(tmplist)

    for edge in edgelist:
        edge.append({"capacity":int(traffic[edge[0]][edge[1]][0]['label'])})
        #edge.append({"label":int(network[edge[0]][edge[1]][0]['label'])})
        
    airTrafficGraph.add_edges_from(edgelist)
    

    airTrafficGraph=removeAntiParallelEdges(airTrafficGraph)
    airTrafficGraph=removeCapConstraint(airTrafficGraph,nodeCaps)
    
    #network=SingleSourceSink(airTrafficGraph, traffic)


    plotGraph(airTrafficGraph)

    
    '''netout = nx.write_dot(airTrafficGraph, "./airgraphout.dot")
    file4 = open("./airgraphout.dot",'r')
    newnet= nx.read_dot(file4)
    print(newnet.to_directed())'''

  
    flow, F =nx.ford_fulkerson(airTrafficGraph, 'S','T')
    #print(flow)
    
    for thing in F:
        print thing, F[thing]
    
    #print(network)
    #unwindFlow(network,airTrafficGraph,F)
##    print nodeCaps
##    print (multiEdgeNodes)
##    print(network.nodes())
##    print("~~~~~~~~~~~~~~~~~~~")
##    print(network["newnode1"]["JFK"][0]['label'])
##    print(network.edges())
##    print(nodeCaps)
##    print(traffic)

    file2.close()

def unwindFlow(network,airTrafficGraph,flow_dict):
    networkNodes = network.nodes()
    networkEdges = network.edges()

    FlowNetwork = nx.DiGraph()
    FlowNetwork = nx.DiGraph(name='FlowNetwork')
    FlowNetwork.add_nodes_from(network)

    for node in flow_dict:
        for neighbor in flow_dict[node]:  

            if ((node, neighbor) in networkEdges):  

                if flow_dict[node][neighbor]!=0:
                   
                    print ((node,neighbor),network[node][neighbor][0]['label'])       
		    print ("fuck you")
            else:
                
                if len(neighbor)==2*len(node):
                    print node,flow_dict[neighbor]
                    if ((node,flow_dict[neighbor].keys()) in networkEdges):
			print("fuck me")
			print(flow_dict[neighbor][node],network[node][flow_dict[neighbor.keys()]][0]['label']) 

                    
def removeAntiParallelEdges(network):
    multiEdgeNodes=[]
    newnodecount =1
    nodes = network.nodes()
    for node1 in nodes:
	for node2 in nodes:
    	    if node1 != node2:
                node1Neighbors = network.neighbors(node1)
                node2Neighbors = network.neighbors(node2)

		if(node1 in node2Neighbors and (node2 in node1Neighbors)): 
                    if ((node1,node2) not in multiEdgeNodes):
                        multiEdgeNodes.append((node2,node1))
                    #print "~~~~~~~~~~~~~~~~~~~"
                    #print(node1+"->"+node2+" capacity: " + str(network[node1][node2]["capacity"]))    
				                         		
	    #do anti-parallel edge removal by adding intermediate node

            if ((node1,node2) in multiEdgeNodes):
                #add node newnode 
                newnode = str(node1)+str(node2)
                newnodecount +=1
                network.add_node(newnode)
                #retrieve value for original edge..store in value
                value = int(network[node1][node2]['capacity'])
                #add edge from node1 to newnode' ..add value
                network.add_edge(node1, newnode, capacity=value) 
                #add edge from newnode to node2.. add value
                network.add_edge(newnode, node2, capacity=value)
                #remove edge node1 and node2 
                network.remove_edge(node1,node2)
                #print(node1+"->"+newnode+" weight: " + str(network[node1][newnode]['capacity']))
                #print(newnode+"->"+node2+" weight: " + str(network[newnode][node2]['capacity']))


    #print(multiEdgeNodes)
    #print("~~~~~~~~~~~~~")
    #print(network.edges())
    return network

def removeCapConstraint(network,nodeCaps):
    nodes = network.nodes()
    edges = network.edges()
    for node in nodes:
        neighbor_dict= {}
        if node in nodeCaps:
            neighbors = network.neighbors(node)
            newnode = node+"'"
            network.add_node(newnode)
            weight = int(nodeCaps[node])
            network.add_edge(node, newnode, capacity=weight)
            for neighbor in neighbors:
                neighbor_dict[neighbor]=network[node][neighbor]['capacity']
                network.remove_edge(node,neighbor)
            for neighbor in neighbor_dict:
                network.add_edge(newnode, neighbor, capacity=neighbor_dict[neighbor])
            #print(newnode+"->"+node+" capacity: " + str(network[newnode][node]['capacity'])) 
    return network

def SingleSourceSink(network,traffic):
    nodes = network.nodes()
    SuperSource = "S"
    SuperSink = "T"
    network.add_node(SuperSource)
    network.add_node(SuperSink)
    for node1 in nodes:
        weight =0
        neighbors= network.neighbors(node1)
        for node2 in neighbors:
            weight += int(network[node1][node2]['capacity'])
        network.add_edge(SuperSource, node1, capacity=weight)
        #print(SuperSource+"->"+node1+" capacity: " + str(network[SuperSource][node1]['capacity']))
    
    for node1 in nodes:
        weight =0
        for node2  in nodes:
            neighbors= network.neighbors(node2)
            if node1 in neighbors:
                weight += int(network[node2][node1]['capacity'])
        network.add_edge(node1, SuperSink , capacity=weight)
        #print(node1+"->"+SuperSink+" weight: " + str(network[node1][SuperSink]['capacity']))
        #print("\n")
    
    return network

def plotGraph(G):
    A = nx.to_agraph(G)
    A.layout('dot', args=' -Nfontsize=10 -Nwidth=".75" -Nheight=".75" -Nmargin=0 -Gfontsize=8')
    A.draw('AirTrafficGraph.png')


if __name__=="__main__":
    main(sys.argv)
