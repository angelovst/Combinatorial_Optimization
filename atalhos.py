import graph_tool.all as gt

class VisitanteAtalhos(gt.BFSVisitor):

	def __init__(self, dist, p, num_vertices):
		self.dist = dist
		self.p = p
		self.num_vertices = num_vertices
		self.primeira_vez = True

	def examine_edge(self, e):
		if self.dist[e.target()] == self.dist[e.source()] + 1:
			self.p[e.target()].append(e.source())

	def discover_vertex(self, u):
		if self.primeira_vez:
			self.dist[u] = 0
			self.primeira_vez = False

	def tree_edge(self, e):
		self.dist[e.target()] = self.dist[e.source()] + 1
		self.p[e.target()].append(e.source())

def atalhos(g):
	
	for v in g.get_vertices():
		dist = g.new_vertex_property("int32_t") 
		p = g.new_vertex_property("vector<int32_t>")
		gt.bfs_search(g, v, VisitanteAtalhos(dist, p, g.num_vertices()))
		g.vertex_properties["distancia" + str(v)] = dist
		g.vertex_properties["p" + str(v)] = p


g = gt.load_graph("search_example.xml")
atalhos(g)
gt.graph_draw(g, pos=g.vp["pos"], vertex_text=g.vp["p0"], vertex_font_size=12, vertex_shape="double_circle",vertex_fill_color="#729fcf", vertex_pen_width=3, output="search_example.pdf")