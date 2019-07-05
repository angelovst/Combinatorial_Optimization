from atalhos import *
import random
import copy

g = gt.collection.data["adjnoun"]
random.seed(1)

valoresOriginais = g.vertex_properties["value"]

vertices = random.sample(range(0, g.num_vertices()), int(g.num_vertices() * 0.5))
brancos = [i for i in range(g.num_vertices()) if i not in vertices]

cores = g.new_vertex_property("string")
g.vp.cor_interna = cores

for i in vertices:
	cores[g.vertex(i)] = VERMELHO if valoresOriginais[g.vertex(i)] == 1.0 else AZUL

for i in brancos:
	cores[g.vertex(i)] = BRANCO
verms = [i for i in vertices if cores[g.vertex(i)] == VERMELHO]
azuis = [i for i in vertices if cores[g.vertex(i)] == AZUL]

#gt.graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=12, vertex_shape="double_circle",vertex_fill_color=cores, vertex_pen_width=3, pos = gt.arf_layout(g, max_iter=0))


