import queue




graph1 = {}
graph2={}
indeg={}
early_starts = {}
dur={}



def get_early():
    q = queue.Queue()
    for key, value in indeg.items():
        if(value==0):
            q.put(key)
    while(not q.empty()):
        node = q.get()
        for val in graph1[node]:
            early_starts[val]=max(early_starts[val], early_starts[node]+dur[node])
            indeg[val]=indeg[val]-1
            if(indeg[val]==0):
                q.put(val)


def build_graphs(data):
    for val in data:
        early_starts.setdefault(val[0], 0)
        indeg.setdefault(val[0], 0)
        graph1.setdefault(val[0], [])
        graph2.setdefault(val[0], [])
        dur.setdefault(val[0], int(val[1]))
    for val in data:
        dependencies=val[2].split(',')
        for dep in dependencies:
            if(dep!='-'): 
                indeg[val[0]]=indeg[val[0]]+1
                graph1[dep].append(val[0])
                graph2[val[0]].append(dep)
    get_early()
    print(early_starts)




