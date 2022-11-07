from graphs.BayesNet import *

class DAG:

    def __init__(self, name, dot=''):
        self.name = name
        self.nx_graph = None
        self.nodes = None
        self.arrows = None
        if dot:
            with open("tempo13.txt", "w") as file:
                file.write(dot)
            self.nx_graph = DotTool.nx_graph_from_dot_file("tempo13.txt")
            self.nodes = list(self.nx_graph.nodes)
            self.arrows = list(self.nx_graph.edges)

    def create_random_bnet(self, nd_to_size):
        bnet = BayesNet.new_from_nx_graph(self.nx_graph)
        print("ccvv\n", bnet)
        for nd in bnet.nodes:
            nd.potential = DiscreteCondPot(False, list(nd.parents).append(nd))
            nd.potential.set_to_random()
            nd.potential.normalize_self()
        return bnet

    @staticmethod
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
                dot += arrow[0] + "_" + str(k+1)\
                    + "->" + arrow[1] + "_" + str(k+1) + ";\n"
        dot += "}"
        return dot


if __name__ == "__main__":

    def main():
        dot = "digraph G {\n" \
              "a->b;\n" \
              "a->s;\n" \
              "n->s,a,b;\n" \
              "b->s\n"\
              "}"
        dag = DAG("test_dag", dot)
        nd_to_size = {}
        for nd in dag.nodes:
            nd_to_size[nd] = 2
        nd_to_size["a"] = 3
        bnet = dag.create_random_bnet(nd_to_size)
        bnet.gv_draw(jupyter=False)
        print(bnet)

    main()

