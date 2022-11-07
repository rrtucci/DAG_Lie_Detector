from BlankCase import *


class Case1(BlankCase):
    """
    https://dreampuf.github.io/GraphvizOnline/

    digraph G {
    a->b [arrowhead=none];
    a->s;
    n->s,a,b;
    b->s
    }

    """

    def __init__(self):
        BlankCase.__init__(self)
        self.pdir_dot, self.links = Case1.get_pdir_dot_and_links()
        self.dag_list, self.dag_to_link_directions = \
            BlankCase.get_dag_list(self.pdir_dot, self.links)

        self.truth_bnet = self.get_truth_bnet()
        self.emp_probs = self.truth_bnet.emp_probs

        self.gcf_calculator = \
            GCF_calculator(self.emp_probs,
                           self.links,
                           self.dag_list,
                           self.dag_to_link_directions)

    @staticmethod
    def get_pdir_dot_and_links():
        pdir_dot = "digraph G {\n" \
                 "a->b[arrowhead=none];\n" \
                 "a->s;\n" \
                 "n->s,a,b;\n" \
                 "b->s;\n" \
                 "}"
        links = [("a", "b")]
        return pdir_dot, links

    def get_truth_bnet(self):
        pdir_dot_addition = ''
        dag = DAG("truth_dag",
                  BlankCase.new_dot_from_pdir_dot(self.pdir_dot,
                                        pdir_dot_addition))
        nd_to_size = {}
        for nd in dag.nodes:
            nd_to_size[nd] = 2
        nd_to_size["a"] = 3
        bnet = dag.create_random_bnet(nd_to_size)
        return TruthBayesNet(self.links, bnet.nodes)





