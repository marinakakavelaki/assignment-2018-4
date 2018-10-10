import sys

class Queue:
    '''
    creates a queue first in first out like list
    '''
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueu(self, item):
        self.items.insert(0, item)

    def deque(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Map():
    '''
    creates a dictionary and provides access  to it with functions
    '''
    def __init__(self,):
        self.D={}


    def insert_in_map(self,v,value):
        self.D[v] = value

    def print_map(self):
        print(self.D)

    def get_value(self,v):
        return self.D[v]


def read_data():
    '''
     Reads data using sys library and creates graph G'
     :return: adjacency list, list of all nodes of the graph
    '''

    global mapping, mapping_one, mapping_two

    with open(sys.argv[1], 'r') as f:
        input1 = f.read()

    lines = input1.split("\n")
    count_lines = 0
    for line in lines:
        count_lines+=1

    m = count_lines

    data = list(map(int, input1.split()))
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    new_edges = []
    mapping = {}
    mapping_one = {}
    mapping_two = {}
    all_nodes = set()
    adj = {}
    for edge in edges:
        a = str(str(edge[0]) + '_one')
        b = str(str(edge[1])+'_two')
        new_edges.append([str(str(edge[0])+'_one'),str(str(edge[1])+'_two')])
        all_nodes.add(a)
        all_nodes.add(b)
        try:
            adj[a].append(b)
        except:
            adj[a] = [b]


        mapping_one[str(str(edge[0])+'_one')]= edge[0]
        mapping_one[str(str(edge[1]) + '_one')] = edge[1]
        mapping_two[str(str(edge[1])+'_two')] = edge[1]
        mapping_two[str(str(edge[0]) + '_two')] = edge[0]

        mapping[str(str(edge[0]) + '_one')] = edge[0]
        mapping[str(str(edge[0]) + '_two')] = edge[0]
        mapping[str(str(edge[1]) + '_one')] = edge[1]
        mapping[str(str(edge[1]) + '_two')] = edge[1]


    for node in set(data):
        check_one = str(str(node)+'_one')
        check_two = str(str(node)+'_two')
        if check_one not in all_nodes:
            adj[check_one] = []
            all_nodes.add(check_one)
        if check_two not in all_nodes:
            adj[check_two] = []
            all_nodes.add(check_two)

    for node in all_nodes:
        if node not in adj.keys():
            adj[node] = []
    return adj, all_nodes

def BreadthFirstSearch(G, B, M):
    '''
    :param G: adjacency list containing graph
    :param B: list of bassist nodes
    :param M: Matchings
    :return: dictionary containing distances for any node from free nodes
    '''
    Q = Queue()
    D = Map()
    for v in G:
        if (v in B) and (M[v] is None):
            D.insert_in_map(v,0)
            Q.enqueu(v)
        else:
            D.insert_in_map(v, len(G)+100)
    while Q.size() > 0:
        c = Q.deque()
        for v in G[c]:
            if D.get_value(v) == len(G)+100:
                if ((c in B) and (M[c] != v)) or ((c not in B) and (v == M[c])):
                    d = D.get_value(c)+1
                    D.insert_in_map(v,d)
                    Q.enqueu(v)
    return D


def DepthFirstSearch(G, s, B, M, D):
    '''
    :param G: adjacency list containing graph
    :param s: current starting node
    :param B: list of bassist nodes
    :param M: Matchings for each node
    :param D: dictionary containing distances for any node from free nodes
    :return: boolean
    '''
    if (s not in B) and (M[s] is None):
        D.insert_in_map(s, len(G)+100)
        return True
    for v in G[s]:
        if ((s in B) and (v != M[s])) or ((s not in B) and (v == M[s])):
            value1= D.get_value(v)
            value2 = D.get_value(s)+1
            if value1 == value2:
                if DepthFirstSearch(G, v, B, M, D):
                     if s in B:
                        M[s] = v
                        M[v] = s
                     return True
    D.insert_in_map(s, len(G)+100)
    return False



def HopcrofKarp(G, B):
    '''
    Implementation of Hopcroft Karp algorithm
    :param G: adjacency list containing graph
    :param B: list of bassist nodes
    :return: Matchings dictionary
    '''
    M = {}
    for v in G:
        M[v] = None

    augmented = True
    while augmented:
        augmented = False
        distances = BreadthFirstSearch(G, B, M)
        for v in B:
            if M[v] is None:
                if DepthFirstSearch(G, v, B, M, distances):
                    augmented = True

    return M

def bfs_transform(graph, start, result):
    '''
    Transforms the result from HopcrofKarp into a path made of the nodes of initial graph G
    '''
    global visited
    visited.append(start)
    result.append(start)
    for next in graph[start]:
        if next not in visited:
            bfs_transform(graph, next, result)
    return result

def find_paths(all_nodes,out_graph):
    '''
    recreating path from initial nodes of graph G
    :param all_nodes: nodes of the graph
    :param out_graph: adjacency list
    :return: routes
    '''
    global visited
    visited = []
    routes = []
    rest_of_nodes = []
    for node in all_nodes:
        result = []
        real_node = node
        if len(out_graph[real_node]) > 0 and real_node not in visited:
            start = real_node
            routes.append(bfs_transform(out_graph, start, result))
        elif len(out_graph[real_node]) == 0 and real_node not in visited:
            rest_of_nodes.append(real_node)

    for node in rest_of_nodes:
        result = []
        if node not in visited:
            start = node
            routes.append(bfs_transform(out_graph, start, result))
    return routes

def create_bassists(adj_list):
    """
    creates bassists list to pass in Hopcroft Karp
    :param adj_list:graph
    :return: bassists sorted according to number of connections of each node. The nodes with less outgoing connections will be placed first.
    """
    sorting_dict = {}
    bassists = []
    for node in mapping_one:
        sorting_dict[node] = len(adj_list[node])

    sorted_by_value = sorted(sorting_dict.items(), key=lambda kv: kv[1])

    for lst in sorted_by_value:
        bassists.append(lst[0])
    return bassists


if __name__=='__main__':
    global mapping
    adj_list, all_nodes = read_data()

    bassists = create_bassists(adj_list)
    M = HopcrofKarp(adj_list, bassists)

    out_graph = {}
    all_nodes = []
    for key in M.keys():
        new_key = mapping[key]
        all_nodes.append(new_key)
        if M[key] is not None:
            new_value = mapping[M[key]]
            try:
                out_graph[new_key].append(new_value)
            except:
                out_graph[new_key]=[new_value]

        for key in all_nodes:
            if key not in out_graph.keys():
                out_graph[key] = []

    routes = find_paths(all_nodes, out_graph)

    print('\n'.join(map(str, routes)))


