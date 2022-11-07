from graphs.BayesNet import *

class TruthBayesNet(BayesNet):

    def __init__(self, links, nodes):
        BayesNet.__init__(self, nodes)
        self.links = links
        # emp_probs = empirical probabilities
        self.emp_probs = {}

    def set_link_to_emp_probs(self):
        link_nd_names = []
        for link in self.links:
            for ampu_st_k in [0,1]:
                if link[ampu_st_k] not in link_nd_names:
                    link_nd_names.append(link[ampu_st_k])
        link_nds = [self.get_node_named(name) for\
                     name in link_nd_names]
        full_pot = link_nds[0].potential
        for ampu_st_k in range(1, len(link_nds)):
            full_pot = full_pot*(link_nds[ampu_st_k].potential)
        nd_name_to_probs = {}
        for nd in link_nds:
            pot_arr = full_pot.get_new_marginal([nd]).pot_arr
            nd_name_to_probs[nd.name] = np.copy(pot_arr)

        link_to_ampu_probs = {}
        for link in self.links: # link= (nd_name_a, nd_name_b)
            size_a = self.get_node_named(link[0]).size
            size_b = self.get_node_named(link[1]).size
            prob_a_bar_do_b = np.zeros((size_b, size_a))
            prob_b_bar_do_a = np.zeros((size_a, size_b))
            for amputee in ["a", "b"]:
                ampu_bnet = cp.deepcopy(self)
                nd_a = ampu_bnet.get_node_named(link[0])
                nd_b = ampu_bnet.get_node_named(link[1])
                if amputee == "a":
                    ampu_nd, not_ampu_nd = nd_a, nd_b
                    ampu_size, not_ampu_size = size_a, size_b
                else:
                    ampu_nd, not_ampu_nd = nd_b, nd_a
                    ampu_size, not_ampu_size = size_b, size_a
                for pa_nd in ampu_nd.parents:
                    ampu_nd.remove_parent(pa_nd)
                for ampu_st_k, ampu_st_name in enumerate(ampu_nd.state_names):
                    ampu_nd.potential = Potential(
                        False,
                        [],
                        pot_arr=np.zeros((ampu_size,)))
                    ampu_nd.potential[(ampu_st_k,)] = 1
                    ord_nodes = list(ampu_bnet.nodes)
                    full_pot = ord_nodes[0].potential
                    for j in range(1, len(link_nds)):
                        full_pot = full_pot*(ord_nodes[j].potential)
                    ampu_pot = full_pot.get_new_marginal(
                        [ampu_nd, not_ampu_nd])
                    if amputee == "a":
                        prob_b_bar_do_a[ampu_st_k, :] = \
                            ampu_pot.pot_arr[ampu_st_k, :]
                    else:
                        prob_a_bar_do_b[:, ampu_st_k] = \
                            np.ampu_pot.pot_arr[:, ampu_st_k]
            link_to_ampu_probs[(link[0], link[1])]= \
                (prob_a_bar_do_b, prob_b_bar_do_a)
            self.emp_probs = [nd_name_to_probs, link_to_ampu_probs]
