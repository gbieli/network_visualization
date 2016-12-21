import pandas
import networkx as nx
import matplotlib.pyplot as plt

#connections = pandas.read_csv("C:\\TMP\\KSA_Verbindungen.csv", header=None, dtype=str)
connections = pandas.read_excel("C:\\TMP\\KSA_Verbindungen.xlsx", sheetname='Sheet1')
connections.columns = ["conn-id", "Switch1", "Verbindung", "Switch2", "Switch2-Port", "Panel", "Panel-Port", "SFP", "Laenge-Patch1", "Laenge-Patch2", "Field0"]

# Initialize the weights dictionary.
weights = {}
# Keep track of keys that have been added once -- we only want edges with a weight of more than 1 to keep our network size manageable.
added_keys = []
# Iterate through each route.
for name, row in connections.iterrows():
    # Extract the source and dest airport ids.
    source = row["Switch2"]
    dest = row["Switch1"]
    # Create a key for the weights dictionary.
    # This corresponds to one edge, and has the start and end of the route.
    key = "{0}_{1}".format(source, dest)
    # If the key is already in weights, increment the weight.
    if key in weights:
        weights[key] += 1
    # If the key is in added keys, initialize the key in the weights dictionary, with a weight of 2.
    elif key in added_keys:
        weights[key] = 2
    # If the key isn't in added_keys yet, append it.
    # This ensures that we aren't adding edges with a weight of 1.
    else:
        added_keys.append(key)

graph = nx.Graph()
# Keep track of added nodes in this set so we don't add twice.
nodes = set()
# Iterate through each edge.
for k, weight in weights.items():
    try:
        # Split the source and dest ids and convert to integers.
        source, dest = k.split("_")
        #source, dest = [int(source), int(dest)]
        # Add the source if it isn't in the nodes.
        if source not in nodes:
            graph.add_node(source, label=str(source))
        # Add the dest if it isn't in the nodes.
        if dest not in nodes:
            graph.add_node(dest)
        # Add both source and dest to the nodes set.
        # Sets don't allow duplicates.
        nodes.add(source)
        nodes.add(dest)

        # Add the edge to the graph.
        graph.add_edge(source, dest, weight=weight)
    except (ValueError, IndexError):
        pass

#pos=nx.spring_layout(graph)

# Draw the nodes and edges.
#nx.draw_networkx_nodes(graph,pos, node_color='red', node_size=10, alpha=0.8)
#nx.draw_networkx_edges(graph,pos,width=1.0,alpha=1)
nx.draw(graph, with_labels=True)

# Show the plot.
plt.show()