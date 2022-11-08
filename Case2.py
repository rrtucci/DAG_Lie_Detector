from BlankCase import *

class Case2(BlankCase):
    """
    https://dreampuf.github.io/GraphvizOnline/
    dot_atlas/case2.dot

    """

    def __init__(self):
        BlankCase.__init__(self)
        self.set_dot_file_path()
        self.pdir_dot = BlankCase.get_pdir_dot(self.dot_file_path)
        self.links = BlankCase.get_links(self.dot_file_path)
        # print("werty", self.links)
        self.dag_list, self.dag_to_link_directions = \
            BlankCase.get_dag_list(self.pdir_dot, self.links)

        self.set_truth_bnet()
        self.emp_probs = self.truth_bnet.emp_probs

        self.gcf_calculator = \
            GCF_calculator(self.emp_probs,
                           self.links,
                           self.dag_list,
                           self.dag_to_link_directions)
    def set_dot_file_path(self):
        self.dot_file_path = "dot_atlas/case2.dot"

    def set_truth_bnet(self):
        # choose any dag from dag_list and add legal structure to its dot
        dag = self.dag_list[0]
        dot_addition = ''
        enhanced_dot = dag.dot.replace("{","{" +dot_addition)
        print('kkklll1', dag.dot)
        print('kkklll2', enhanced_dot)
        dag = DAG("truth_dag", enhanced_dot)
        # print("qqwwee", dag.nodes, dag.arrows)
        nd_to_size = {}
        for nd in dag.nodes:
            nd_to_size[nd] = 2
        nd_to_size["a"] = 3
        bnet = TruthBayesNet.create_random_bnet(
            dag.nodes,
            dag.arrows,
            nd_to_size)
        self.truth_bnet = TruthBayesNet(bnet)

if __name__ == "__main__":

    def main(jupyter, draw):
        case = Case2()
        case.run(jupyter=jupyter, draw=draw)

    main(jupyter=False, draw=True)

