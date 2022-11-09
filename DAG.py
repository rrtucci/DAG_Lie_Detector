from graphs.BayesNet import *
from TruthBayesNet import *

class DAG:
    """

    """

    def __init__(self, name, basic_dot):
        """

        Parameters
        ----------
        name
        basic_dot
        """
        self.name = name
        self.basic_dot = basic_dot
        self.nodes = None
        self.arrows = None
        with open("tempo13.txt", "w") as file:
            file.write(basic_dot)

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

    def __str__(self):
        """

        Returns
        -------

        """
        s = "\nname: " + self.name
        s += "\nnodes: "
        for nd in self.nodes:
            s += nd + ", "
        s += "\narrows: "
        for arrow in self.arrows:
            s += repr(arrow) + ", "
        return s


if __name__ == "__main__":

    def main():
        dot = "digraph G {\n" \
              "a->b;\n" \
              "a->s;\n" \
              "n->s,a,b;\n" \
              "b->s\n"\
              "}"
        print(DAG("G", dot))
        dag_list = [DAG("G_1", dot), DAG("G_2", dot)]
        print(DAG.get_dag_list_dot(dag_list))

    main()

