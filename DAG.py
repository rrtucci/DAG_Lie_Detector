from graphs.BayesNet import *
from TruthBayesNet import *

class DAG:

    def __init__(self, name, dot):
        self.name = name
        self.nodes = None
        self.arrows = None
        with open("tempo13.txt", "w") as file:
            file.write(dot)

        self.nodes, self.arrows = \
            DotTool.read_dot_file("tempo13.txt")


    @staticmethod
    def get_dag_list_dot(dag_list):
        """
        dag_list : list[DAG]

        Returns
        -------

        """
        dot = "digraph {\n"
        for k, dag in enumerate(dag_list):
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

        dag_list = [DAG("G_1", dot), DAG("G_2", dot)]
        print(DAG.get_dag_list_dot(dag_list))

    main()

