from graphs.BayesNet import *
from DAG import *
from pprint import pprint
import random
random.seed(13)

class TruthBayesNet(BayesNet):
    """
    The constructor of this class takes as input 'bnet' which is an object
    of the class BayesNet. This class uses 'bnet' to simulate the empirical
    probabilities emp_probs.

    Attributes
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

    links: list[tuple[str, str]]

    """

    def __init__(self, bnet):
        """

        Parameters
        ----------
        bnet: BayesNet
        """
        BayesNet.__init__(self, bnet.nodes)
        self.links = []
        for pa_nd in bnet.nodes:
            for ch_nd in pa_nd.children:
                self.links.append((pa_nd.name, ch_nd.name))

        # emp_probs = empirical probabilities
        self.emp_probs = {}
        self.set_emp_probs()

    def set_emp_probs(self):
        """
        This method sets the empirical probabilities self.emp_probs.

        Returns
        -------
        None

        """
        nodes = list(self.nodes)
        # for nd in nodes:
        #     print("vvvvs", nd.name, nd.size, nd.potential.pot_arr.shape)
        full_pot = nodes[0].potential
        for ampu_k in range(1, len(nodes)):
            full_pot = full_pot*(nodes[ampu_k].potential)
        nd_name_to_probs = {}
        for nd in nodes:
            pot_arr = full_pot.get_new_marginal([nd]).pot_arr
            nd_name_to_probs[nd.name] = pot_arr
            # print("llkhg", nd.name, nd.size)
        # print("gfrt", nd_name_to_probs)
        link_to_ampu_probs = {}
        for link in self.links:
            size_0 = self.get_node_named(link[0]).size
            size_1 = self.get_node_named(link[1]).size
            prob_0_bar_do_1 = np.zeros((size_1, size_0))
            prob_1_bar_do_0 = np.zeros((size_0, size_1))
            for amputee in [0, 1]:
                # print("cccA")
                ampu_bnet = cp.deepcopy(self)
                # print("ccccB", ampu_bnet)
                nd_0 = ampu_bnet.get_node_named(link[0])
                nd_1 = ampu_bnet.get_node_named(link[1])
                if amputee == 0:
                    ampu_nd, not_ampu_nd = nd_0, nd_1
                    ampu_size, not_ampu_size = size_0, size_1
                else:
                    ampu_nd, not_ampu_nd = nd_1, nd_0
                    ampu_size, not_ampu_size = size_1, size_0
                original_parents = list(ampu_nd.parents)
                for pa_nd in original_parents:
                    ampu_nd.remove_parent(pa_nd)
                    # print("ooppp", ampu_nd.name)
                # print("dddff", link, amputee, "\n", ampu_bnet)
                for ampu_k in range(ampu_size):
                    ampu_nd.potential = Potential(
                        False,
                        [ampu_nd],
                        pot_arr=np.zeros((ampu_size,)))
                    ampu_nd.potential.pot_arr[ampu_k] = 1
                    # print("lkknm", link, amputee, ampu_k, "\n", ampu_bnet)
                    nds = list(ampu_bnet.nodes)
                    full_pot = nds[0].potential
                    for j in range(1, len(self.nodes)):
                        full_pot = full_pot*(nds[j].potential)
                    ampu_pot = full_pot.get_new_marginal(
                        [ampu_nd, not_ampu_nd])
                    # print("hhjki-link-amputee-k",
                    #       link, amputee, ampu_k, "\n", ampu_pot)
                    if amputee == 0:
                        prob_1_bar_do_0[ampu_k, :] = \
                            ampu_pot.pot_arr[ampu_k, :]
                    else:
                        prob_0_bar_do_1[ampu_k, :] = \
                            ampu_pot.pot_arr[ampu_k, :]
            # list L can't be used as key to dictionary
            # but tuple(L) or repr(L) can be
            link_to_ampu_probs[link]= \
                [prob_0_bar_do_1, prob_1_bar_do_0]
            self.emp_probs = [nd_name_to_probs, link_to_ampu_probs]

    @staticmethod
    def create_random_bnet(nodes,
                           arrows,
                           nd_to_size):
        """
        This method returns a BayesNet object whose structure is given by
        'nodes' and 'arrows'. The TPM (transition probability matrix) for
        each node is created at random, with the only constraint being that
        the number of states of each node be as specified by the input
        'nd_to_size'.

        Parameters
        ----------
        nodes: list[str]
            example: ['a', 'b', 'c']
        arrows: list[tuple[str, str]]
            example: [('a', 'b'), ('a', 'c')]
        nd_to_size: dict[str, int]
            dictionary mapping node name to its size (i.e., the number of
            values or states)

        Returns
        -------
        BayesNet

        """
        bnet_nodes = []
        for k, node_name in enumerate(nodes):
            nd = BayesNode(k, name=node_name)
            nd.size = nd_to_size[node_name]
            bnet_nodes.append(nd)
        bnet = BayesNet(set(bnet_nodes))
        for arrow in arrows:
            pa_nd = bnet.get_node_named(arrow[0])
            child_nd = bnet.get_node_named(arrow[1])
            child_nd.add_parent(pa_nd)

        # print("ccvv", bnet.nodes)
        for nd in bnet_nodes:
            ord_nodes = list(nd.parents) + [nd]
            # print("llkjh", ord_nodes)
            nd.potential = DiscreteCondPot(False, ord_nodes)
            nd.potential.set_to_random()
            nd.potential.normalize_self()
        # print("aadf", bnet)
        return bnet

if __name__ == "__main__":

    def main(draw=False):
        dot = "digraph G {\n" \
              "a->b;\n" \
              "a->s;\n" \
              "n->s,a,b;\n" \
              "b->s\n" \
              "}"
        dag = DAG("test_dag", dot)
        nd_to_size = {}
        for nd in dag.nodes:
            nd_to_size[nd] = 2
        nd_to_size["a"] = 3
        bnet = TruthBayesNet.create_random_bnet(
            dag.nodes,
            dag.arrows,
            nd_to_size)
        print("Truth bnet (used to simulate empirical probs):")
        if draw:
            bnet.gv_draw(jupyter=False)
        print(bnet)

        truth_bnet = TruthBayesNet(bnet)
        # print("ddfgg", truth_bnet)
        emp_probs = truth_bnet.emp_probs
        nd_name_to_probs, link_to_ampu_probs = emp_probs
        print('simulated empirical single node probs:')
        pprint(nd_name_to_probs)
        print("\nsimulated empirical do-query probs:")
        for link in truth_bnet.links:
            prob_0_bar_do_1, prob_1_bar_do_0 = \
                link_to_ampu_probs[link]
            print("\nlink=", link)
            print("prob_0_bar_do_1:")
            pprint(prob_0_bar_do_1)
            print("prob_1_bar_do_0:")
            pprint(prob_1_bar_do_0)

    main(draw=False)