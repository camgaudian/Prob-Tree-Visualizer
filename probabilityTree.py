# Written by Cameron Gaudian and Ethan Omwoyo
# 12.06.24

import matplotlib.pyplot as plt
import networkx as nx

def create_probability_tree_from_events(graph, current_node, depth, max_depth, events, cumulative_prob):
    """
    Recursively creates a probability tree based on a given list of events with probabilities.
    Each edge is labeled with the overall probability of reaching the event.
    """
    if depth >= max_depth:  # base case
        return

    for event, prob in events:
        # Create a new child node labeled with the event name
        child_node = f"{current_node}-{event}"
        # Calculate the cumulative probability for the child node
        overall_prob = cumulative_prob * prob
        # Add the edge with the overall probability as an attribute
        graph.add_edge(current_node, child_node, probability=overall_prob)
        # Recur for the child node
        create_probability_tree_from_events(graph, child_node, depth + 1, max_depth, events, overall_prob)


def get_depth(node, graph, root):
    """
    Returns the depth of the node in the tree based on the shortest path from the root.
    """
    return nx.shortest_path_length(graph, source=root, target=node)


# Create an empty directed graph
G = nx.DiGraph()

# List used to create the probability tree
prob_events = []

def get_event_list():
    num_events = int(input("\nPlease enter the number of possible outcomes per event: "))
    
    while True:
        sumProb = 0

        for i in range(num_events):
            name = input(f"\nChoose a name or symbol for outcome {i + 1}: ")
            prob = float(input(f"\nEnter the probability of '{name}' occurring (0.0 - 1.0): "))
            prob_events.append((name, prob))

        for item in prob_events:
            sumProb += item[1]

        if sumProb == 1.0:
            break
        else:
            prob_events.clear()
            print("\nOops. The sum of the probabilities for your outcomes should be 1.")
            print("Let's start over and try again.")

event_name = "\n" * 4 + input("\n\nChoose a name for your event: ")
get_event_list()

# Add the root node and build the tree
G.add_node(event_name)

# Depth of the tree (how many times a the event will happen)
max_depth = int(input("\nPlease enter the number of times the event will occur: "))

# use function from earlier to generate our probability tree
print("\n\nGenerating Tree...\n\n")
create_probability_tree_from_events(G, event_name, 0, max_depth, prob_events, 1)

# Assign subset based on depth (shortest path from root)
for node in G.nodes:
    G.nodes[node]['subset'] = get_depth(node, G, event_name)

# Get all the unique depth levels
depths = list(set(nx.get_node_attributes(G, 'subset').values()))
depths.sort()

# Create a list to hold the positions
pos = {}

# For each depth, assign nodes to a horizontal line (based on depth)
for depth in depths:
    nodes_at_depth = [node for node, data in G.nodes(data=True) if data['subset'] == depth]
    num_nodes = len(nodes_at_depth)
    
    # Calculate positions for nodes at each depth level
    angle_step = 2 * 3.14159 / num_nodes if num_nodes > 0 else 1  # Evenly distribute nodes around a circle
    x_offset = 2 * depth  # Move the layers apart horizontally
    for i, node in enumerate(nodes_at_depth):
        x = x_offset
        y = 3 * (i - (num_nodes - 1) / 2)  # Vertically space out nodes in each level
        pos[node] = (x, y)

# Visualize the tree
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=8, arrows=True)

# Draw edge labels with overall probabilities
edge_labels = {(u, v): f"{d['probability'] * 100:.2f}%" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("")
plt.show()  # Display the plot