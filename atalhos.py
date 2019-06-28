import graph_tool.all as gt

VERMELHO = '#FF0000'
AZUL = '#0000ff'
BRANCO = '#ffffff'
CINZA = '#808080'
AZUL_CLARO = '#ccccff'
VERMELHO_CLARO = '#ffcccc'

class VisitanteAtalhos(gt.BFSVisitor):

	def __init__(self, dist, p, num_vertices):
		self.dist = dist
		self.p = p
		self.num_vertices = num_vertices
		self.primeira_vez = True

	#This is invoked on every out-edge of each vertex after it is discovered.
	def examine_edge(self, e):
		if self.dist[e.target()] == self.dist[e.source()] + 1:
			self.p[e.target()].append(e.source())

	#This is invoked when a vertex is encountered for the first time.
	def discover_vertex(self, u):
		if self.primeira_vez:
			self.dist[u] = 0
			self.primeira_vez = False

	#This is invoked on each edge as it becomes a member of the edges that form the search tree.
	def tree_edge(self, e):
		self.dist[e.target()] = self.dist[e.source()] + 1
		self.p[e.target()].append(e.source())

def atalhos(g):
	
	for v in g.get_vertices():
		dist = g.new_vertex_property("int32_t") 
		p = g.new_vertex_property("vector<int32_t>")
		gt.bfs_search(g, v, VisitanteAtalhos(dist, p, g.num_vertices()))
		g.vertex_properties["distancia" + str(v)] = dist
		# property [v][w] = vizinhos de w em caminhos mais curtos entre w e v
		g.vertex_properties["p" + str(v)] = p


'''
def pertence(g, s, z):
	marcados = g.new_vertex_property("bool")
	g.vp.marcados = marcados
	ret = pertenceRec(g, s, z)
	del g.vertex_properties["marcados"]
	return ret
'''	

def pertence(g, s, z):
	marcados = g.new_vertex_property("bool")
	g.vp.marcados = marcados
	falsos = [False for _ in g.vertices()]	

	for var in z: 
		ret = pertenceInicio(g, s, var, falsos[:])
		if ret:
			del g.vertex_properties["marcados"]		
			return True
	
	del g.vertex_properties["marcados"]
	return False


def pertenceInicio(g, s, i, falsos):
	g.vp.marcados.a = falsos
	return pertenceRec(g, s, i)	

# Retorna vértices de z que pertencem ao fecho convexo de s
def pertencem(g, s, z):
	marcados = g.new_vertex_property("bool")
	g.vp.marcados = marcados
	falsos = [False for _ in g.vertices()]	
	ret = [i for i in z if pertenceInicio(g, s, i, falsos[:])]
	del g.vertex_properties["marcados"]
	return ret

def pertenceRec(g, s, z):
	if z in s:
		return True
	if g.vp.marcados[s[0]]:
		return False

	g.vp.marcados[s[0]] = True

	aux = s[0]
	for v in s[1:]:
		for i in g.vp["p" + str(v)][aux]:			
			s[0] = i
			if(pertenceRec(g, s, z)):
				s[0] = aux
				return True
	
	s[0] = aux
	return False

"""
 g: Graph
 s1: One color Vertices
 s2: Opposite color Vertices
 s: set of uncolored Vertices

 returns True if hull(v, w), hull(y, z), and s intersect, and False otherwise
"""		
def cruzam(g, s1, s2, s):
	marcados = g.new_vertex_property("bool")
	g.vp.marcados = marcados
	falsos = [False for _ in g.vertices()]

	for i in s:
		pertence_s1 = pertenceInicio(g, s1, i, falsos)
		if pertence_s1:
			pertence_s2 = pertenceInicio(g, s2, i, falsos)
			if pertence_s2:
				del g.vertex_properties["marcados"]
				return True
	
	del g.vertex_properties["marcados"]
	return False





