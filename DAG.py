from DotTool import *
from graphs.BayesNet import *

class DAG:

    def __init__(self, name, dot=''):
        self.name = name
        self.nx_graph = None
        self.nodes = None
        self.arrows = None
        if dot:
            with open("tempo.txt", "w") as file:
                file.write(dot)
            self.nx_graph = DotTool.nx_graph_from_dot_file("tempo.txt")
            self.nodes = list(self.nx_graph.nodes)
            self.arrows = list(self.nx_graph.edges)

    def create_random_bnet(self, nd_to_size):
        bnet = BayesNet.new_from_nx_graph(self.nx_graph)
        for nd in bnet.nodes:
            nd.potential = DiscreteCondPot(False, list(nd.parents) + nd)
            nd.potential.set_to_random()
            nd.potential.normalize_self()
        return bnet

    def get_dag_list_dot(dag_list):
        """
        dag_list : list[DAG]

        Returns
        -------

        """
        dot = ''
        for k, dag in enumerate(dag_list):
            dot = "DiGraph {\n"
            for arrow in dag.arrows:
                dot += arrow[0] + "_" + str(k)\
                    + "->" + arrow[1] + "_" + str(k) + ";\n"
        dot += "}"
        return dot




