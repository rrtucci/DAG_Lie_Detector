from BlankCase import *


class Case1(BlankCase):
    """
    The constructor for this class should use the following dot_file_path.
    See docstring for class BlankCase for more info.

    dot_atlas/case1.dot

    Attributes
    ----------

    """

    def __init__(self, dot_file_path, emp_probs=None):
        BlankCase.__init__(self, dot_file_path, emp_probs=emp_probs)

    def get_truth_bnet(self):
        """
        This method returns an instance of TruthBayesNet

        Returns
        -------
        TruthBayesNet

        """
        # choose any dag from dag_list and add legal structure to its dot
        dag = self.dag_list[0]
        dot_addition = ''
        enhanced_dot = dag.basic_dot.replace("{", "{" + dot_addition)
        dag = DAG("truth_dag", enhanced_dot)
        # print("qqwwee", dag.nodes, dag.arrows)
        print("\nWe are choosing a truth bnet with the same structure as G_1")
        nd_to_size = {}
        for nd in dag.nodes:
            nd_to_size[nd] = 2
        nd_to_size["a"] = 3
        bnet = TruthBayesNet.create_random_bnet(
            dag.nodes,
            dag.arrows,
            nd_to_size)
        truth_bnet = TruthBayesNet(bnet)
        return truth_bnet


if __name__ == "__main__":

    def main(jupyter, draw):
        case = Case1("dot_atlas/case1.dot")
        case.run(jupyter=jupyter, draw=draw)

    main(jupyter=False, draw=True)

