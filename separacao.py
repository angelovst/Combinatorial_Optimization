from gurobipy import *

def listaDe(k, l, tuplas):
	for par in tuplas[k]:
		if l == par[0]:
			return par[1]
	return None


def separacao(model, where):
	
	if where == GRB.Callback.MIPNODE:
		if model.cbGet(GRB.Callback.MIPNODE_STATUS) == GRB.Status.OPTIMAL:
			print("======================================================")
			x = model.cbGetNodeRel(model._vars)
			for i in model._coloridos:
				for cand in model._tuplas[i]:
					j = cand[0]
					for par in itertools.product(cand[1],cand[1]):
						k = par[0]
						l = par[1]
						if k < l and x[i] + x[j] + x[k] + x[l] < 1.95:				
							lista = listaDe(k,l,model._tuplas)
							if lista != None:
								if i in lista and j in lista:
									model.cbCut(model._vars[i] + model._vars[j] + model._vars[k] + model._vars[l] >= 2)
									print(model._vars[i] + model._vars[j] + model._vars[k] + model._vars[l] >= 2)
									#Imnprimir os valores das variáveis >> Tarefa
									return

