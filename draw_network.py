# Importイベント発生時に動作
# model_infoからデータを引っ張ってきて、ネットワーク図を作成

import json
from utils.info_holder import InfoHolder
from netgraph import Graph, InteractiveGraph, EditableGraph
import igraph as ig
import matplotlib.pyplot as plt

class NetworkDrawer:
    def __init__(self, model_instance):
        self.nodes = model_instance.get_node()
        self.edges = model_instance.get_edge()

    def draw_network(self):
        # グラフの情報を返す
        edge_idx_array = [(self.nodes.index(i[0]), self.nodes.index(i[1])) for i in self.edges]
    
        g = ig.Graph(directed=True)
        g.add_vertices(len(self.nodes))
        g.add_edges(edge_idx_array)
        # plot_instance = InteractiveGraph(g)

        return g