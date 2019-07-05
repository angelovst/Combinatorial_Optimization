from gurobipy import *
from instancia import *
from separacao import *
import itertools

# This example formulates and solves the following simple MIP model:
#  min
#        sum_{i in V} x[i] 
#  subject to
#        x[i] + x[j] + x[k] >= 1, (i,j in VERMELHO and k in AZUL) or (i,j in AZUL and k in VERMELHO) and k in H({i,j})
#        [x[i] binary for i in V] 

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
	x = m.addVars([g.vertex_index[v] for v in g.get_vertices()], vtype=GRB.BINARY, name="x") 

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
			par_verm[1] += [z for z in pertencem(g, [verm, par_verm[0]], azuis)]
			[m.addConstr(x[verm] + x[par_verm[0]] + x[z] >= 1, nome(verm, par_verm[0], z)) for z in par_verm[1]]
			#print([nome(par_verm[0], par_verm[1], z) for z in pertencem(g, par_verm[0], par_verm[1], azuis)])
	
	print(3)

	for azul in azuis:
		for par_azul in tuplas[azul]:
			#nome = str(par_azul[0]) + '_' + str(par_azul[1]) + '_' + str(z)
			par_azul[1] += [z for z in pertencem(g, [azul, par_azul[0]], verms)]
			[m.addConstr(x[azul] + x[par_azul[0]] + x[z] >= 1, nome(azul, par_azul[0], z)) for z in par_azul[1]]
	
	print(4)
	'''		
	# Add constraint: x[i] + x[j] + x[k] + x[l] >= 1			
	for pares in itertools.product([(a, b[0]) for a in azuis for b in tuplas[a]], [(a, b[0]) for a in verms for b in tuplas[a]]):
		if (cruzam(g, [pares[0][0], pares[0][1]], [pares[1][0], pares[1][1]], brancos)):
			nomes = str(pares[0][0]) + '_' + str(pares[0][1]) + '_' + str(pares[1][0]) + '_' + str(pares[1][1])
			m.addConstr(x[pares[0][0]] + x[pares[0][1]] + x[pares[1][0]] + x[pares[1][1]] >= 1, "c" + nomes)				
	'''
	print(5)

	for v in g.get_vertices():
		x[g.vertex_index[v]].start = 0.0

	if len(verms) > len(azuis):
		for i in azuis:
			x[i].start = 1.0
	else:
		for i in verms:
			x[i].start = 1.0
		

	# Optimize model
	m._vars = x
	m._tuplas = tuplas
	m._verms = verms
	m._azuis = azuis
	m._brancos = brancos
	m._coloridos = verms + azuis
	m._g = g
	m.Params.LazyConstraints = 1 
	m.optimize(separacao)
	#m.optimize()


	cores = g.vertex_properties["cor_interna"]
	cor_borda =  copy.deepcopy(cores)

	for i in m._coloridos:
		if x[i].x > 0.9:
			cor_borda[g.vertex(i)] = BRANCO
			print('%s %g' % (x[i].varName, x[i].x))
	for i in brancos:
		cor_borda[g.vertex(i)] = CINZA

	azuis_solucao = [i for i in azuis if x[i].x < 0.9]
	for i in pertencem(g, azuis_solucao, brancos):
		cores[g.vertex(i)] = AZUL_CLARO

	verms_solucao = [i for i in verms if x[i].x < 0.9]
	for i in pertencem(g, verms_solucao, brancos):
		cores[g.vertex(i)] = VERMELHO_CLARO

	for v in g.get_vertices():
			if cores[v] == BRANCO:
				temBranco = True

	while temBranco:
		for v in g.get_vertices():
			if cores[v] == BRANCO:
				contadorAzul = 0
				contadorVerm = 0
				for viz in g.vertex(v).all_neighbors():
					if cores[g.vertex(viz)] == VERMELHO or cores[g.vertex(viz)] == VERMELHO_CLARO:
						contadorVerm += 1
					if cores[g.vertex(viz)] == AZUL or cores[g.vertex(viz)] == AZUL_CLARO:
						contadorAzul += 1
				if contadorVerm > contadorAzul:
					cores[v] = VERMELHO_CLARO
				elif contadorVerm < contadorAzul:
					cores[v] = AZUL_CLARO
				else:
					cores[v] = VERMELHO_CLARO
		temBranco = False
		for v in g.get_vertices():
			if cores[v] == BRANCO:
				temBranco = True


	gt.graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=12, vertex_shape="double_circle",vertex_fill_color=cores, vertex_color = cor_borda, vertex_pen_width=3, output="huhu.pdf")

	print('Obj: %g' % m.objVal)

except GurobiError as e:
	print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
	print('Encountered an attribute error')

