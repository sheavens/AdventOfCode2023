import networkx as nx
import community  # python-louvain library

# Create a sample graph
G = nx.karate_club_graph()

# Apply the Louvain algorithm to find communities
partition = community.best_partition(G)

# Print the resulting communities
print("Node: Community")
for node, community_id in partition.items():
    print(f"{node}: {community_id}")

# Visualization (optional)
import matplotlib.pyplot as plt
from networkx import spring_layout

# Assign colors to nodes based on their community
colors = [partition[node] for node in G.nodes]

# Draw the graph with nodes colored by community
pos = spring_layout(G)
nx.draw(G, pos, node_color=colors, with_labels=True, cmap=plt.cm.RdYlBu, font_weight='bold')
plt.show()