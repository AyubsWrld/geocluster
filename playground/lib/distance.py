import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

location = 'Edmonton, Alberta, Canada'

G = ox.graph_from_place(location, network_type='drive')

origin_address = '4501 30 Ave NW, Edmonton, AB'
destination_address = '4225 118 Ave NW, Edmonton, AB'

origin = ox.geocode(origin_address)
destination = ox.geocode(destination_address)

orig_node = ox.distance.nearest_nodes(G, origin[1], origin[0])
dest_node = ox.distance.nearest_nodes(G, destination[1], destination[0])

route = nx.shortest_path(G, orig_node, dest_node, weight='length')

fig, ax = ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k')

route_edges = G.edges(route)
route_geometry = [G.edges[edge]['geometry'] for edge in route_edges]
route_bounds = ox.utils_geo.bbox_from_point(origin, dist=3000)  # Adjust distance as needed

circle = plt.Circle((origin[1], origin[0]), 0.03, color='red', fill=False, linestyle='dashed')  # Adjust radius as needed
ax.add_artist(circle)

plt.title(f'Shortest Route from {origin_address} to {destination_address}')
plt.axis('equal')
plt.show()
