import networkx as nx
import matplotlib.pyplot as plt
import operator
import collections
from random import randint
import time
import csv
import pandas as pd
#########################################################



"""
start=datetime.now()
print("Exec. Time: ", datetime.now()-start)
"""


######################################################
def HasNode(G,node):
    if(G.has_node(node)==True):
        return True
    else:
        return False

def GeneralInfos(my_graph):
    print(nx.info(TestGraph))
    print('Is Connected?: ',nx.is_connected(my_graph))
    print('Is Directed? : ',nx.is_directed(my_graph))

	
#DegreeHistogram

def DegHistogram(my_graph): #Takes graph name
    G = my_graph
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    # print "Degree sequence", degree_sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    
    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')
    
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
    ax.set_xscale('log')

    plt.show()

def FindCentrality(my_graph):
    return nx.degree_centrality(my_graph)
	
def FindMaxInDict(dict):

    try:
        return max(dict.items(),key=operator.itemgetter(1))[0]
    except KeyError:
        print('Some of your nodes is/are not available in the network!')
	
def FindHopNumbers(path,node1,node2):
    try:
        temp=path[str(node1)][str(node2)]
        return len(temp)-1
    except KeyError:
        print('Some of your nodes is/are not available in the network!')

def DictToGraph(dict):
    lists = sorted(dict.items())
    x,y=zip(*lists)
	
    plt.plot(x,y)
    ax.set_xscale('log')
    plt.show()
    
def FindNeighbors(G,node):
    tmp= list(nx.neighbors(G,str(node)))
    return tmp

def astarpath(graph,node1,node2):

    while(HasNode(graph,node1)==True and HasNode(graph,node2)==True):
        tmp=nx.astar_path(graph,node1,node2)
        return tmp
    return print("Mistaken nodes, Try again.")

def GraphCreator(my_list):
    G=nx.Graph()
    i=0
    j=1
    while(i<len(my_list)-1):  
        G.add_edge(int(my_list[i]),int(my_list[j]))
        i=i+1
        j=j+1
    return G

def AllNeighbors(Graph,path):
    x1=list()
    i=0
    while(i<len(path)):
        x1.append(FindNeighbors(Graph,path[i]))
        i=i+1
    return x1
                
def GraphWithNeighbors(Sub,neighborList,path):
    i=0
    j=0
    while(i<len(path)):
        j=0
        while(j<len(neighborList[i])):
            Sub.add_edge(int(path[i]), int(neighborList[i][j]))
            j=j+1
        i=i+1

    nx.draw_networkx(Sub)

def RandomNodes(TestGraph):
    value = randint(0,nx.number_of_nodes(TestGraph))
    return str(value)

def RemoveBlanks(path):
    df = pd.read_csv(path)
    df.to_csv('output.csv', index=False)
###################################################################
    


################################################################
class Test():
    def __init__(self,address):
        self.path=address
        
    def getMainGraph(self):
        return nx.read_edgelist(self.path)
    
    def checkPath(self,node1,node2):
        if(nx.has_path(self.getMainGraph(),node1,node2)==True):
            return True
        else:
            return False
            
    def timeComparison(self,total_iterations):
        with open ('Gnutella31.csv', mode='a+') as csv_file:
            fieldnames = ['Start','End','Algorithm','HopNumber','Time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            i=1
            while(i<total_iterations):
                node1=RandomNodes(self.getMainGraph())
                node2=RandomNodes(self.getMainGraph())       
                print("From ", node1, " To ", node2, "İteration Number : ", i )
                
                if(self.checkPath(node1,node2)==True):
                    
                
                    start = time.process_time()
                    self.astar=astarpath(self.getMainGraph(),node1,node2)
                    time1=time.process_time()-start        
                    writer.writerow({'Start': node1 , 'End': node2, 'Algorithm':'Astar', 'HopNumber': len(self.astar), 'Time': time1})
                
                    start = time.process_time()
                    self.dij = nx.single_source_dijkstra(self.getMainGraph(),node1,node2)
                    time2=time.process_time()-start
                    writer.writerow({'Start': node1 , 'End': node2, 'Algorithm':'Dijkstra', 'HopNumber': len(self.dij[1]), 'Time': time2})        
        
                    start = time.process_time()
                    self.bellmanford = nx.single_source_bellman_ford(self.getMainGraph(),node1,node2)
                    time3=time.process_time()-start       
                    writer.writerow({'Start': node1 , 'End': node2, 'Algorithm':'Bellman-Ford', 'HopNumber': len(self.bellmanford[1]), 'Time': time3})
                    i=i+1
                else:
                    i=i+1
                    continue
        subGraph=GraphCreator(self.astar)
        neighbor_list=AllNeighbors(self.getMainGraph(),self.astar)
        GraphWithNeighbors(subGraph,neighbor_list,self.astar)
        
    def getAstar(self):
        return self.astar
    def getDijkstra(self):
        return self.dij
    def getBellmanFord(self):
        return self.bellmanford
    

File1 = Test('p2p-gnutella31.txt')

File1.timeComparison(701)

RemoveBlanks('Gnutella31.csv')


#################Test Codes
"""
g=nx.read_edgelist('p2p-gnutella31.txt')
mytest=astarpath(g, '0','19') #Two random nodes selected in nodes
CreateSubGraph=GraphCreator(mytest)
neighbors=AllNeighbors(g,mytest)
GraphWithNeighbors(CreateSubGraph,neighbors,mytest)
"""

