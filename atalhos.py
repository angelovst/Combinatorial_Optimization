import graph_tool.all as gt

VERMELHO = '#FF0000'
AZUL = '#729fcf'
BRANCO = '#ffffff'

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


def pertence(g, v, w, z):
	marcados = g.new_vertex_property("bool")
	g.vp.marcados = marcados
	ret = pertenceRec(g, v, w, z)
	del g.vertex_properties["marcados"]
	return ret

def pertenceInicio(g, v, w, i, falsos):
	g.vp.marcados.a = falsos

	return pertenceRec(g, v, w, i)

def pertencem(g, v, w, z):
	marcados = g.new_vertex_property("bool")
	g.vp.marcados = marcados
	falsos = [False for _ in g.vertices()]	
	ret = [i for i in z if pertenceInicio(g, v, w, i, falsos)]
	del g.vertex_properties["marcados"]
	return ret

def pertenceRec(g, v, w, z):
	if v == z or w == z:
		return True

	if g.vp.marcados[w]:
		return False

	g.vp.marcados[w] = True

	for i in g.vp["p" + str(v)][w]:
		if(pertenceRec(g, v, i, z)):
			return True

	return False
		
def cruzam(g, v, w, y, z, s):
	marcados = g.new_vertex_property("bool")
	g.vp.marcados = marcados

	falsos = [False for _ in g.vertices()]

	for i in s:
		if pertenceInicio(g, v, w, i, falsos) and pertenceInicio(g, y, z, i, falsos):
			del g.vertex_properties["marcados"]
			return True
	
	del g.vertex_properties["marcados"]
	return False