from graphs.BayesNet import *
from TruthBayesNet import *


class DAG:
    """
    This is a very simple class whose constructor takes as input a
    "basic_dot" string. Here is an example of a basic dot:

            dot = "digraph G {\n" \
              "a->b;\n" \
              "a->s;\n" \
              "n->s,a,b;\n" \
              "b->s\n"\
              "}"

    Note that each line referring to arrows ends with a semicolon, except
    the last one, for which the semicolon is optional. Note that it contains
    no edge attributes, so all edges are directed.

    From the basic dot, this class extracts the names of the nodes of the
    DAG and puts them in a list 'self.nodes'. It also extracts the edges (
    e.g., ('a', 'b')) of the DAG and puts them in a list 'self.arrows'.

    Attributes
    ----------
    arrows: tuple[str, str]
    basic_dot: str
    name: str
    nodes: list[str]

    """

    def __init__(self, name, basic_dot):
        """

        Parameters
        ----------
        name: str
            name given to the DAG being created
        basic_dot: str
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
        This method returns a dot string created from a list of DAG instances.

        Parameters
        ----------
        dag_list : list[DAG]

        Returns
        -------
        str

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
        This method determines what happens when you do a print(object),
        where object is an object of this class.

        Returns
        -------
        None

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

