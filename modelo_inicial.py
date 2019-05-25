from gurobipy import *
from classifica import *
import itertools

# This example formulates and solves the following simple MIP model:
#  min
#        sum_{i in V} x[i] 
#  subject to
#        x[i] + x[j] + x[k] >= 1, (i,j in VERMELHO and k in AZUL) or (i,j in AZUL and k in VERMELHO) and k in H({i,j})
#        [x[i] binary for i in V] 
	
try:

	# Create a new model
	m = Model("Classifica")

	# Create variables
	x = [m.addVar(vtype=GRB.BINARY, name="x_{}".format(g.vertex_index[v])) for v in g.get_vertices()] 
	
	# Set objective
	m.setObjective(sum(x[v] for v in g.get_vertices()), GRB.MINIMIZE)

	# Add constraint: x[i] + x[j] + x[k] >= 1
	atalhos(g)

	nome = lambda a, b, c : "c" + str(a) + '_' + str(b) + '_' + str(c)

	for par_verm in itertools.product(verms, verms):
		if (par_verm[0] < par_verm[1]):
			#nome = str(par_verm[0]) + '_' + str(par_verm[1]) + '_' + str(z)
			[m.addConstr(x[par_verm[0]] + x[par_verm[1]] + x[z] >= 1, nome(par_verm[0], par_verm[1], z)) for z in azuis if pertence(g, par_verm[0], par_verm[1], z)]

	# Optimize model
	m.optimize()

	for v in m.getVars():
		print('%s %g' % (v.varName, v.x))

	print('Obj: %g' % m.objVal)

except GurobiError as e:
	print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
	print('Encountered an attribute error')