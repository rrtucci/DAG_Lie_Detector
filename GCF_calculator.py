from itertools import product
import numpy as np


class GCF_calculator:
    """
    This class calculates the GCF (goodness of causal fit) for a list of DAG
    objects inputted to its constructor via the variable 'dag_list'. GCF is
    a causal fitness score that is defined in the following paper

    https://github.com/rrtucci/goodness-c-fit/blob/master/gcf.pdf

    The constructor of this class requires as input 'emp_probs' (empirical
    probabilities), 'dag_list' (a list of DAG instances), 'links' (a list of
    the undirected edges (i.e., links) ) and a dictionary
    'dag_to_link_directions' mapping each dag to the directions of the links
    listed in 'links'.

    'emp_probs' can be calculated from the data by some external program and
    handed to this one. Alternatively, it can be simulated by the class
    TruthBayesNet.

    Attributes
    ---------
    dag_list: list[DAG]
    dag_to_gcf: dict[DAG, float]
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
    link_to_heights_01: dict[tuple[str, str], list[float, float]]
    links: tuple[str, str]

    """

    def __init__(self,
                 emp_probs,
                 links,
                 dag_list,
                 dag_to_link_directions):
        """

        Parameters
        ----------
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

        links: list[tuple[str,str]]
        dag_list: list[DAG]
        dag_to_link_directions: dict[DAG, list[str]]
        """
        self.emp_probs = emp_probs
        self.links = links
        self.dag_list = dag_list
        self.dag_to_link_directions = dag_to_link_directions

        self.link_to_heights_01 = {}
        self.dag_to_gcf = {}
        self.set_link_to_heights_01()
        self.set_dag_to_gcf()

    def set_link_to_heights_01(self):
        """
        This method sets the parameter 'self.link_to_heights_01' which is a
        dictionary that maps each link to a list of two floats height_0,
        height_1. For a link ('a_0', 'a_1'), height_0 (resp., height_1) is
        the height of node 'a_0' (resp., 'a_1')

        Returns
        -------
        None

        """
        nd_name_to_probs, link_to_ampu_probs = self.emp_probs
        # print("ddccv", link_to_ampu_probs)
        # print("llllk", self.links)
        for link in self.links:
            nd_0, nd_1 = link[0], link[1]
            prob_0_bar_do_1, prob_1_bar_do_0 = \
                link_to_ampu_probs[link]
            prob_0, prob_1 = \
                nd_name_to_probs[nd_0], nd_name_to_probs[nd_1]
            size_0, size_1 = prob_1_bar_do_0.shape
            height_0 = 0
            height_1 = 0
            for k_0, k_1 in product(range(size_0), range(size_1)):
                x = prob_0[k_0]*prob_1[k_1]
                y_do_0 = np.log(prob_1[k_1]/prob_1_bar_do_0[k_0, k_1])
                y_do_1 = np.log(prob_0[k_0]/prob_0_bar_do_1[k_1, k_0])
                height_0 += x*y_do_0
                height_1 += x*y_do_1

            self.link_to_heights_01[link] = [height_0, height_1]

    def set_dag_to_gcf(self):
        """
        This method sets the parameter 'self.dag_to_gcf' which is a
        dictionary that maps each DAG object (in the list self.dag_list) to
        its GCF.

        Returns
        -------
        None

        """
        for dag in self.dag_list:
            d_sum = 0
            abs_d_sum = 0
            for k_link, link in enumerate(self.links):
                points_to_1 = \
                    (self.dag_to_link_directions[dag][k_link] == "0->1")
                height_0, height_1 = self.link_to_heights_01[link]
                height_diff = np.abs(height_0-height_1)
                if height_0 > height_1:
                    height_1_is_smaller = True
                else:
                    height_1_is_smaller = False
                reward = - 1
                if points_to_1 == height_1_is_smaller:
                    reward = 1
                d_sum += reward*height_diff
                abs_d_sum += height_diff
            self.dag_to_gcf[dag] = d_sum / max(abs_d_sum, 1e-10)

    def print_heights_01(self):
        """
        This method prints the two floats height_0 and height_1 for each
        element of 'self.links'.

        Returns
        -------
        None

        """
        for link in self.links:
            height_0, height_1 = self.link_to_heights_01[link]
            print("link", ", height_0", ", height_1")
            print(link, "\t", '%.5f' % height_0, "\t", '%.5f' % height_1)

    def print_GCFs(self):
        """
        This method prints the float GCF for each DAG object in the list
        'self.dag_list'.

        Returns
        -------
        None

        """
        for dag, gcf in self.dag_to_gcf.items():
            print("dag=", dag.name, ",\tGCF=", "%.5f" % gcf)
