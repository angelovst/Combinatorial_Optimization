from gurobipy import *
from classifica import *
from separacao import *
import itertools

# This example formulates and solves the following simple MIP model:
#  min
#        sum_{i in V} x[i] 
#  subject to
#        x[i] + x[j] + x[k] >= 1, (i,j in VERMELHO and k in AZUL) or (i,j in AZUL and k in VERMELHO) and k in H({i,j})
#        [x[i] binary for i in V] 
'''
def naoArestas(g, v1, v2):

	tuplas = []

	for i in v1:
		naoVizinho = [False for _ in g.get_vertices()]
		for j in v2:
			naoVizinho[j] = (j > i)
		for j in g.vertex(i).all_neighbors():
			naoVizinho[g.vertex_index[j]] = False

		a = [(g.vertex_index[i], g.vertex_index[j]) for j in g.get_vertices() if naoVizinho[g.vertex_index[j]]]

		tuplas += a

	return tuplas
'''
def naoArestas(g, v, tuplas):

	for i in v:
		naoVizinho = [False for _ in g.get_vertices()]
		for j in v:
			naoVizinho[j] = (j > i)
		for j in g.vertex(i).all_neighbors():
			naoVizinho[g.vertex_index[j]] = False

		a = [[g.vertex_index[j], []] for j in g.get_vertices() if naoVizinho[g.vertex_index[j]]]

		tuplas[g.vertex_index[i]] = a



try:

	# Create a new model
	m = Model("Classifica")

	# Create variables
	x = [m.addVar(vtype=GRB.BINARY, name="x_{}".format(g.vertex_index[v])) for v in g.get_vertices()] 

	print(1)
	
	# Set objective
	m.setObjective(sum(x[v] for v in g.get_vertices()), GRB.MINIMIZE)

	atalhos(g)

	# Add constraint: x[i] + x[j] + x[k] >= 1
	nome = lambda a, b, c : "c" + str(a) + '_' + str(b) + '_' + str(c)
	tuplas = [None for _ in g.get_vertices()]

	naoArestas(g, verms, tuplas)
	naoArestas(g, azuis, tuplas)

	print(2)

	for verm in verms:
		for par_verm in tuplas[verm]:
			#print(str(par_verm[0]) + '_' + str(par_verm[1]))
			par_verm[1] += [z for z in pertencem(g, verm, par_verm[0], azuis)]
			[m.addConstr(x[verm] + x[par_verm[0]] + x[z] >= 1, nome(verm, par_verm[0], z)) for z in par_verm[1]]
			#print([nome(par_verm[0], par_verm[1], z) for z in pertencem(g, par_verm[0], par_verm[1], azuis)])

	print(3)

	for azul in azuis:
		for par_azul in tuplas[azul]:
			#nome = str(par_azul[0]) + '_' + str(par_azul[1]) + '_' + str(z)
			par_azul[1] += [z for z in pertencem(g, azul, par_azul[0], verms)]
			[m.addConstr(x[azul] + x[par_azul[0]] + x[z] >= 1, nome(azul, par_azul[0], z)) for z in par_azul[1]]

	print(4)
	'''		
	# Add constraint: x[i] + x[j] + x[k] + x[l] >= 1			
	for pares in itertools.product([(a, b[0]) for a in azuis for b in tuplas[a]], [(a, b[0]) for a in verms for b in tuplas[a]]):
		if (cruzam(g, pares[0][0], pares[0][1], pares[1][0], pares[1][1], brancos)):
			nomes = str(pares[0][0]) + '_' + str(pares[0][1]) + '_' + str(pares[1][0]) + '_' + str(pares[1][1])
			m.addConstr(x[pares[0][0]] + x[pares[0][1]] + x[pares[1][0]] + x[pares[1][1]] >= 1, "c" + nomes)				
	'''
	print(5)

	m.write("qualquercoisa.lp")
	# Optimize model
	m._vars = x
	m._tuplas = tuplas
	m._coloridos = verms + azuis
	m.optimize(separacao)


	for v in m.getVars():
		print('%s %g' % (v.varName, v.x))

	print('Obj: %g' % m.objVal)

except GurobiError as e:
	print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
	print('Encountered an attribute error')