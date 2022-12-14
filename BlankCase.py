from DAG import *
from TruthBayesNet import *
from GCF_calculator import *
from itertools import product
import graphviz as gv
from IPython.display import display, Image
from PIL.Image import open as open_image

edge_attr = "[arrowhead=none,color=red]"


class BlankCase:
    """
    This is an abstract class. Subclasses of this class, such as Case1, 
    Case1_2, etc. are the frontend interfaces for running this app for a 
    particular usecase. BlankCase is much longer than its subclasses and 
    does all the common heavylifting work, whereas its subclasses like Case1 
    are designed to be as lean as possible, and only do work that is ultra 
    usecase specific. 

    The constructor of this class, and also the constructor of its
    subclasses, requires as input 'dot_file_path' and 'emp_probs'.

    'dot_file_path' is the path to a dot file located in the folder
    'dot_atlas'. A dot file is a text file in the dot language that
    specifies a graph (i.e., network). A dot file or dot string is used as
    input for the graphviz rendering engine.

    'emp_probs' are the empirical probabilities. A value for 'emp_probs' is 
    an optional input for the constructor of this class. If a value for 
    'emp_probs' isn't provided by the user, a random one will be 
    generated/simulated by the class TruthBayesNet. Class TruthBayesNet is 
    called that because it generates a Bayesian Network (bnet) that 
    represents "the truth", and uses that bnet to simulate the empirical 
    probabilities. 
 
    Attributes
    ----------
    dag_list: list[DAG]
    dag_to_link_directions: dict[DAG, list[str]]
    emp_probs: list[dict, dict]
        empirical probabilities. More specifically, emp_probs equals
        [node_name_to_probs, link_to_ampu_probs]

        'node_name_to_probs' dict[str, np.array] is a dictionary that
        maps each node name like 'a' to its probability 1-dim numpy array
        like P(a).

        'link_to_ampu_probs' dict[tuple[str, str], [np.array, np.array]]
        is a dictionary that maps a link to its amputated probabilities,
        which are 2 numpy arrays P(a|do(b)) and P(b|do( a)) for a link (
        'a', 'b').
    gcf_calculator: GCF_calculator
    links: tuple[str, str]
    pdir_dot: str
    truth_bnet: TruthBayesNet

    """

    def __init__(self, dot_file_path, emp_probs=None):
        """

        Parameters
        ----------
        dot_file_path: str
            path to dot file in 'dot_atlas' folder
        emp_probs: list[dict, dict]
            empirical probabilities. More specifically, emp_probs equals
            [node_name_to_probs, link_to_ampu_probs]

            'node_name_to_probs' dict[str, np.array] is a dictionary that
            maps each node name like 'a' to a probability 1-dim numpy array
            like P(a).

            'link_to_ampu_probs' dict[tuple[str, str], [np.array, np.array]]
            is a dictionary that maps a link to its amputated probabilities,
            which are 2 numpy arrays P(a|do(b)) and P(b|do( a)) for a link (
            'a', 'b').

        """
        self.pdir_dot = BlankCase.get_pdir_dot(dot_file_path)
        self.links = BlankCase.get_links(dot_file_path)
        # print("werty", self.links)
        self.dag_list, self.dag_to_link_directions = \
            BlankCase.get_dag_list(self.pdir_dot, self.links)

        self.emp_probs = emp_probs
        # not used if emp_probs is not None
        self.truth_bnet = None
        if emp_probs is None:
            self.truth_bnet = self.get_truth_bnet()
            self.emp_probs = self.truth_bnet.emp_probs

        self.gcf_calculator = \
            GCF_calculator(self.emp_probs,
                           self.links,
                           self.dag_list,
                           self.dag_to_link_directions)

    def get_truth_bnet(self):
        """
        This method returns a truth BayesNet which simulates the empirical
        probabilities.

        Returns
        -------
        TruthBayesNet

        """
        assert False

    @staticmethod
    def get_pdir_dot(dot_file_path):
        """
        This method simply reads a file located at 'dot_file_path' and
        returns its content string. The content string is expected to be a
        dot string specifying a partially directed (pdir) graph.

        Parameters
        ----------
        dot_file_path: str

        Returns
        -------
        str

        """
        with open(dot_file_path, "r") as f:
            pdir_dot = f.read()
        return pdir_dot

    @staticmethod
    def get_links(dot_file_path):
        """
        In this app, a link is an undirected edge of a graph (i.e.,
        network), specified as a tuple of two strings that are the names of
        the two nodes that the link connects; for instance, ('a', 'b') is a
        link between nodes 'a' and 'b'.

        This method reads a dot file located at 'dot_file_path'. That dot
        file is expected to specify a partially directed graph, which is a
        graph with both directed and undirected (links) edges. This method
        returns a list of the links it finds in the dot file it reads.

        Parameters
        ----------
        dot_file_path: str

        Returns
        -------
        list[tuple[str,str]]

        """
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
        This method returns a list of instances of the class DAG. These DAGs
        (directed acyclic graphs) are constructed by giving a direction,
        in all possible ways, to the undirected edges (links) in a partially
        directed (pdir) graph. This pdir graph is described by the dot
        string 'pdir_dot', which has links 'links'.

        Parameters
        ----------
        pdir_dot: str
        links: list[tuple[str,str]]

        Returns
        -------
        list[DAG]

        """
        def get_no_attr_dag_dot(pdir_dot, links, dir_links):
            """
            This internal method returns a dot string with no undirected
            edges and no edge attributes. The output dot of this method is
            obtained by stripping away the edge attribute edge_attr = "[
            arrowhead=none, color=red]" from every line in pdir_do where it
            occurs, and then replacing the formerly undirected edge by a
            directed one that is stipulated by dir_links.


            Parameters
            ----------
            pdir_dot: str
            links: list[tuple[str, str]]
                for example, [('a', 'b'), ('b', 'c')]
            dir_links: list[str]
                for example, ["a->b", "b->c"]

            Returns
            -------
            str

            """
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
            dir_links = []  # directed links
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
        """
        This method draws the dot file 'dot'.

        Parameters
        ----------
        dot: str
        jupyter: bool
            Use jupyter=False if drawing to a console, and jupyter=True if
            drawing to a jupyter notebook.


        Returns
        -------
        None

        """
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
        """
        This method runs the whole app. It writes a lot of text as standard
        output and draws a lot of DAGs using graphviz. It documents all the
        stages required for calculating GCF (goodness of causal fit) for a
        bunch of DAGs.

        Parameters
        ----------
        jupyter: bool
        draw: bool

        Returns
        -------
        None

        """
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
        self.gcf_calculator.print_GCFs()
