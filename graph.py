import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def show_graph(data, early_starts, late_finish, dur, delay, crit_path):
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add start node
    start_node = 'st'
    G.add_node(start_node)
    
    # Add tasks and dependencies to the graph
    for val in data:
        task_name = val[0]
        early_start_time = early_starts[task_name]
        late_finish_time = late_finish[task_name]
        
        # Calculate early finish and late start
        early_finish_time = early_start_time + dur[val[0]]
        late_start_time = late_finish_time - dur[val[0]]
        
        # Add the task node
        G.add_node(task_name)
        
        # Add edges based on dependencies
        dependencies = val[2].split(',')
        for dep in dependencies:
            if dep == "-":
                G.add_edge(start_node, task_name)
            else:
                G.add_edge(dep, task_name)

    # Calculate layers for multipartite layout and set as node attribute
    for node in G.nodes():
        layer = get_layer(node, G)
        G.nodes[node]['layer'] = layer  # Set layer as a node attribute

    # Create a layout based on the layers using the 'layer' attribute
    pos = nx.multipartite_layout(G, subset_key='layer')

    # Create a figure
    plt.figure(figsize=(10, 6))

    # Draw the graph without nodes
    nx.draw(G, pos, with_labels=False, node_color='white', node_size=0, 
            font_size=15, arrows=True, arrowstyle='-|>', arrowsize=20)

    # Draw square nodes and numbers inside them
    for node, (x, y) in pos.items():
        if node != start_node:
            # Determine if the node is on the critical path
            is_critical = node in crit_path
            node_color = 'red' if is_critical else 'lightblue'  # Set node color based on critical path

            # Draw a square node
            square_size = 0.08  # Size of the square
            square = Rectangle((x - square_size / 2, y - square_size / 2), square_size, square_size,
                               facecolor=node_color, edgecolor='black')
            plt.gca().add_patch(square)

            # Draw the numbers and task name inside the square
            early_start_time = early_starts[node]
            early_finish_time = early_start_time + dur[node]
            late_start_time = late_finish[node] - dur[node]
            late_finish_time = late_finish[node]
            delay_value = delay.get(node, 0)

            # Positioning offsets for the numbers
            offset = 0.02  # Adjust this value to move the numbers closer or further from the center

            # Draw numbers in the node
            plt.text(x - offset, y + offset, str(early_start_time), ha='center', va='center', fontsize=10)
            plt.text(x + offset, y + offset, str(early_finish_time), ha='center', va='center', fontsize=10)
            plt.text(x - offset, y - offset, str(late_start_time), ha='center', va='center', fontsize=10)
            plt.text(x + offset, y - offset, str(late_finish_time), ha='center', va='center', fontsize=10)
            plt.text(x, y + 3 * offset, str(delay_value), ha='center', va='center', fontsize=10)

            # Add the task name at the center of the square
            plt.text(x, y, node, ha='center', va='center', fontsize=10, fontweight='bold')

    # Add critical path text at a fixed location in the plot (bottom center) and reverse the critical path list
    plt.figtext(0.5, 0.01, f'Critical Path: {" -> ".join(crit_path[::-1])}', ha='center', fontsize=12, fontweight='bold')

    # Show the graph
    plt.axis('off')  # Turn off the axis
    plt.show()

def get_layer(node, G):
    """ Determine the layer of the node based on its dependencies. """
    if node == 'st':  # Start node
        return 0
    layer = 0
    predecessors = list(G.predecessors(node))
    while predecessors:
        layer += 1
        new_predecessors = []
        for pred in predecessors:
            new_predecessors.extend(G.predecessors(pred))
        predecessors = new_predecessors
    return layer

