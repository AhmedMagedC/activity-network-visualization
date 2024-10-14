import queue
from graph import show_graph



graph1 = {}
graph2={}
indeg1={}
indeg2={}
early_starts = {}
late_finish = {}
dur={}
delay={}
crit_path=[]
end_point=""




def get_early():
    q = queue.Queue()
    for key, value in indeg1.items():
        if(value==0):
            q.put(key)
    while(not q.empty()):
        node = q.get()
        for val in graph1[node]:
            early_starts[val]=max(early_starts[val], early_starts[node]+dur[node])
            indeg1[val]=indeg1[val]-1
            if(indeg1[val]==0):
                q.put(val)


def build_graphs(data):
    for val in data:
        early_starts.setdefault(val[0], 0)
        late_finish.setdefault(val[0], 1e9)
        indeg1.setdefault(val[0], 0)
        indeg2.setdefault(val[0], 0)
        graph1.setdefault(val[0], [])
        graph2.setdefault(val[0], [])
        dur.setdefault(val[0], int(val[1]))
    for val in data:
        dependencies=val[2].split(',')
        for dep in dependencies:
            if(dep!='-'): 
                indeg1[val[0]]=indeg1[val[0]]+1
                indeg2[dep]=indeg2[dep]+1
                graph1[dep].append(val[0])
                graph2[val[0]].append(dep)
    get_early()
    end_point=get_late()
    get_delay(data)
    crit_path.append(end_point)
    calc_crit_path(end_point)
    print(crit_path)
    show_graph(data, early_starts, late_finish, dur, delay, crit_path)


def get_late():
    # max_early_finish=max(max_early_finish,early_starts[key]+dur[key])
    max_early_finish=0
    q = queue.Queue()
    for key, value in indeg2.items():
        if(value==0):
            q.put(key)
            if(max_early_finish<early_starts[key]+dur[key]):
                max_early_finish=early_starts[key]+dur[key]
                end_point=key
            
    for key, value in indeg2.items():
        if(value==0):
           late_finish[key]=max_early_finish
    
    while(not q.empty()):
        node = q.get()
        for val in graph2[node]:
            late_finish[val]=min(late_finish[val], late_finish[node]-dur[node])
            indeg2[val]=indeg2[val]-1
            if(indeg2[val]==0):
                q.put(val)
    return end_point
                
def get_delay(data):
    for val in data:
        delay.setdefault(val[0], late_finish[val[0]]-(early_starts[val[0]]+dur[val[0]]))
        

def calc_crit_path(node):
    for val in graph2[node]:
        if(delay[val]==0):
            crit_path.append(val)
            calc_crit_path(val)
            return



