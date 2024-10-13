import networkx as nx
import matplotlib.pyplot as plt

def show_graph(data):
        # Create a graph
        G = nx.DiGraph()
        
        node_labels={}
        start_node='st'
        G.add_node(start_node)
        node_labels.setdefault(start_node,"st")
        for val in data:
                task_name=val[0]
                duration=val[1]
                node_labels.setdefault(val[0],"%c\n%d" % (task_name,int(duration)))
                dependencies=val[2].split(',')
                G.add_node(task_name)
                for dep in dependencies:
                        if(dep=="-"):
                                G.add_edge(start_node,task_name)
                        else:
                                G.add_edge(dep,task_name)
                        
       
        # Draw the graph
        nx.draw(G, with_labels=True, labels=node_labels, node_color='lightblue', node_size=1700, 
        font_size=15, arrows=True, arrowstyle='-|>', arrowsize=20)

        # Show the graph
        plt.show()

# show_graph([])
