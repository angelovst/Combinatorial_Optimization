from atalhos import *
import random

g = gt.load_graph("haha.xml")

verms = random.sample(range(0, g.num_vertices()), g.num_vertices() * 0.3)
azuis = random.sample([for i in range(0, g.num_vertices()) if i not in verms], g.num_vertices() * 0.2)
brancos = [i for i in range(g.num_vertices()) if i not in verms and i not in azuis]

cores = g.new_vertex_property("string")

for i in verms:
	cores[g.vertex(i)] = VERMELHO
for i in azuis:
	cores[g.vertex(i)] = AZUL
for i in brancos:
	cores[g.vertex(i)] = BRANCO

gt.graph_draw(g, pos=g.vp["pos"], vertex_text=g.vertex_index, vertex_font_size=12, vertex_shape="double_circle",vertex_fill_color=cores, vertex_pen_width=3, output="search_example.pdf")