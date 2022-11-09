from DAG import *
from TruthBayesNet import *
from GCF_calculator import *
from itertools import product
import graphviz as gv
from IPython.display import display, Image
from PIL.Image import open as open_image

edge_attr = "[arrowhead=none,color=red]"

class BlankCase:

    def __init__(self):
        self.dot_file_path = None
        self.pdir_dot = None
        self.links = None
        self.dag_list = None
        self.dag_to_link_directions = None
        self.gcf_calculator = None

        # not used if directory 'link_to_emp_probs' given as input
        self.truth_bnet = None

    @staticmethod
    def get_pdir_dot(dot_file_path):
        with open(dot_file_path, "r") as f:
            pdir_dot = f.read()
        return pdir_dot

    @staticmethod
    def get_links(dot_file_path):
        links = []
        with open(dot_file_path) as f:
            in_lines = f.readlines()
        for line in in_lines:
            if edge_attr in line:
                line = line.replace(edge_attr, "")
                line = line.replace(";", "")
                split_list = line.split(sep="->")
                nd_0 = split_list[0].strip()
                nd_1 = split_list[1].strip()
                # links must be tuples
                # They can't be lists because they will be
                # used as keys to dictionaries
                links.append((nd_0, nd_1))
        return links


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
        def get_no_attr_dag_dot(pdir_dot, links, dir_links):
            x = pdir_dot
            # print("yyyj1", x)
            # trim all empty space
            x = x.replace(" ", "")
            # print("yyyj1.1", x)
            num_links = len(links)
            for k in range(num_links):
                old_str = links[k][0] + "->" + links[k][1] + edge_attr
                new_str = dir_links[k]
                x = x.replace(old_str, new_str)
            # print("yyyj2", x)

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
                      get_no_attr_dag_dot(pdir_dot, links, dir_links))
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


    def run(self, jupyter=False, draw=False):
        if self.truth_bnet:
            print("Truth bnet (used to simulate empirical probs):")
            if draw:
                self.truth_bnet.gv_draw(jupyter)
            print(self.truth_bnet)
        print("Partially Directed graph G_pd:")
        print(self.pdir_dot)
        if draw:
            BlankCase.draw_dot(self.pdir_dot, jupyter)
        print("DAGs for which GCF will be calculated"
              " (non-maximal generation of G_pd)")
        for dag in self.dag_list:
            print(dag)
        if draw:
            BlankCase.draw_dot(
                DAG.get_dag_list_dot(self.dag_list),
                jupyter)
        print("\nlink to heights:")
        self.gcf_calculator.print_heights_01()
        print("\nGCF for each dag:")
        self.gcf_calculator.print_GFCs()
