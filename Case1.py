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
        self.PD_dot, self.links = Case1.get_PD_dot_and_links()
        self.dag_list, self.dag_to_link_directions = \
            BlankCase.get_dag_list(self.PD_dot, self.links)

        self.truth_bnet = self.get_truth_bnet()
        self.link_to_emp_probs = self.truth_bnet.emp_probs

        self.GCF_calculator = \
            GCF_calculator(self.links,
                           self.dag_list,
                           self.link_to_emp_probs,
                           self.dag_to_link_directions)

    def get_PD_dot_and_links(blank=None):
        PD_dot = "digraph G {" \
                 "a->b[arrowhead=none];" \
                 "a->s;" \
                 "n->s,a,b;" \
                 "b->s}"
        links = [("a", "b")]
        return PD_dot, links

    def get_truth_bnet(self):
        PD_dot_addition = ''
        if PD_dot_addition:
            new_dot = self.PD_dot.replace('{', '{' + PD_dot_addition)
        else:
            new_dot = self.PD_dot
        dag = DAG("truth_dag", new_dot)

        nd_to_size = {}
        for nd in dag.nodes:
            nd_to_size[nd] = 2
        bnet = dag.create_random_bnet(nd_to_size)
        return TruthBayesNet(self.links, bnet.nodes)





