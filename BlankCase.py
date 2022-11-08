from DAG import *
from TruthBayesNet import *
from GCF_calculator import *
from itertools import product
import graphviz as gv
from IPython.display import display, Image
from PIL.Image import open as open_image
import random
random.seed(13)

class BlankCase:

    def __init__(self):
        self.pdir_dot = None
        self.links = None
        self.dag_list = None
        self.dag_to_link_directions = None
        self.gcf_calculator = None

        # not used if directory 'link_to_emp_probs' given as input
        self.truth_bnet = None

    @staticmethod
    def get_dag_list(pdir_dot, links):
        """

        Parameters
        ----------
        pdir_dot : str
        links

        Returns
        -------

        """
        def get_dot(pdir_dot, links, dir_links):
            x = str(pdir_dot)
            # trim all white space, including empty space and \n, \t
            "".join(x.split())
            num_links = len(links)
            for k in range(num_links):
                old_str = links[k][0] + "->" + links[k][1] + "[arrowhead=none]"
                new_str = dir_links[k]
                x = x.replace(old_str, new_str)
            # newline after every semicolon
            x.replace(";", ";\n")

            return x

        dag_list = []
        dag_to_link_directions = {}
        dag_index = 0
        for link_directions in product(("0->1", "1->0"), repeat=len(links)):
            dag_index += 1
            dir_links = [] # directed links
            for k, link in enumerate(links):
                # "<-" not valid in dot language
                if link_directions[k] == "0->1":
                    # link = ("0", "1")
                    # link_direction == "0->1" if points to 1
                    dir_links.append(link[0] + "->" + link[1])
                else:
                    dir_links.append(link[1] + "->" + link[0])
            dag = DAG("G_" + str(dag_index), 
                      get_dot(pdir_dot, links, dir_links))
            dag_list.append(dag)
            dag_to_link_directions[dag] = link_directions
        # for dag in dag_list:
        #     print("6667", dag)
        return dag_list, dag_to_link_directions

    @staticmethod
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

    @staticmethod
    def new_dot_from_pdir_dot(pdir_dot, pdir_dot_addition):
        if pdir_dot_addition:
            new_dot = pdir_dot.replace('{', '{' + pdir_dot_addition)
        else:
            new_dot = str(pdir_dot)
        new_dot = new_dot.replace("[arrowhead=none]", "")
        return new_dot

    def run(self, jupyter=False, draw=False, verbose=True):
        if self.truth_bnet:
            print("Truth bnet (used to simulate emp_probs):")
            if draw:
                self.truth_bnet.gv_draw(jupyter)
            print(self.truth_bnet)
        print("Partially Directed (PD) graph:")
        if draw:
            BlankCase.draw_dot(self.pdir_dot, jupyter)
        print(self.pdir_dot)
        print("DAG list (non-maximal generation of PD graph):")
        if draw:
            BlankCase.draw_dot(
                DAG.get_dag_list_dot(self.dag_list),
                jupyter)
        for dag in self.dag_list:
            print(dag)
        print("\nGCF for each dag:")
        for dag, gcf in self.gcf_calculator.dag_to_gcf.items():
            print("dag=", dag.name, ",\tGCF=", gcf)
