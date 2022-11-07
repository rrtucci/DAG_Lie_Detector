from DAG import *
from TruthBayesNet import *
from GCF_calculator import *
from itertools import product
import graphviz as gv
from IPython.display import display, Image
from PIL.Image import open as open_image

class BlankCase:

    def __init__(self):
        self.PD_dot = None
        self.links = None
        self.dag_list = None
        self.dag_to_link_directions = None
        self.truth_bnet = None # not used if link_to_emp_probs given
        self.GCF_calculator = None

    def get_dag_list(PD_dot, links):
        """

        Parameters
        ----------
        PD_dot : str
        links

        Returns
        -------

        """
        def get_dot(dag_arrows):
            # trim all white space, including empty space, \n, \t
            x = "".join(PD_dot.split())
            "".join(x.split())
            for arrow in dag_arrows:
                old_arrow = arrow[0] + "->" + arrow[1] + "[arrowhead=none]"
                x = x.replace(old_arrow, arrow)
            # newline after every semicolon
            x.replace(";", ";\n")
            return x

        dag_list = []
        dag_to_link_directions = {}
        dag_index = -1
        for link_directions in product((0, 1), repeat=len(links)):
            dag_index += 1
            dag_arrows = []
            for k, link in enumerate(links):
                # "<-" not valid in dot language
                if link_directions[k] == 0:
                    dag_arrows.append(link[0] + "->" + link[1])
                else:
                    dag_arrows.append(link[1] + "->" + link[0])
            dag = DAG("G_" + str(dag_index), get_dot(dag_arrows))
            dag_list.append(dag)
            dag_to_link_directions[dag] = link_directions

        return dag_list, dag_to_link_directions

    def draw_dot(dot, jupyter):
        # using display(s) will draw the graph but will not embed it
        # permanently in the notebook. To embed it permanently,
        # must generate temporary image file and use Image().
        # display(s)
        s = gv.Source(dot)
        x = s.render("tempo", format='png', view=False)
        if jupyter:
            display(Image(x))
        else:
            open_image("tempo.png").show()

    def run(self, jupyter=False, verbose=False):
        if self.truth_bnet:
            print("Truth bnet, from which emp probs calculated:")
            self.truth_bnet.gv_draw(jupyter)
            print(self.truth_bnet)

        print("Partially Directed (PD) graph:")
        BlankCase.draw_dot(self.PD_dot, jupyter)
        print("DAG list (non-maximal generation of PD graph):")
        BlankCase.draw_dot(
            DAG.get_dag_list_dot(self.dag_list),
            jupyter)
        for dag, gcf in self.GCF_calculator.dag_to_gcf:
            print("dag name=", dag.name, "GCF=", gcf)
