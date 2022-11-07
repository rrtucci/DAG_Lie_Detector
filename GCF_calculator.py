from itertools import product
import numpy as np

class GCF_calculator:
    def __init__(self,
                 links,
                 dag_list,
                 emp_probs,
                 dag_to_link_directions):
        self.links = links
        self.dag_list = dag_list
        self.emp_probs = emp_probs
        self.dag_to_link_directions = dag_to_link_directions

        self.link_to_ab_hospi = {}
        self.dag_to_gcf = {}
        self.set_link_to_ab_hospi()
        self.set_dag_to_gcf()

    def set_link_to_ab_hospi(self):
        nd_to_probs, link_to_ampu_probs = self.emp_probs
        # nd_to_size = {nd:int(nd_to_probs[nd].shape) for\
        #             nd in nd_to_probs.keys()}

        for link in self.links:
            nd_a, nd_b = link[0], link[1]
            # size_a, size_b = nd_to_size[nd_a], nd_to_size
            prob_a_bar_do_b, prob_b_bar_do_a = link_to_ampu_probs[link]
            prob_a, prob_b = nd_to_probs[nd_a], nd_to_probs[nd_b]
            size_a, size_b = prob_b_bar_do_a.shape
            hospi_a = 0
            hospi_b = 0
            for k_a, k_b in product(range(size_a), range(size_b)):
                x = prob_a[k_a]*prob_b[k_b]
                y_a = np.log(prob_b[k_b]/prob_b_bar_do_a[k_a, k_b])
                y_b = np.log(prob_a[k_a]/prob_a_bar_do_b[k_b, k_a])
                hospi_a += x*y_a
                hospi_b += x*y_b

            self.link_to_ab_hospi[link] = [hospi_a, hospi_b]

    def set_dag_to_gcf(self):
        for dag in self.dag_list:
            d_sum = 0
            abs_d_sum = 0
            for k_link, link in enumerate(self.links):
                if self.dag_to_link_directions[dag][k_link]==0:
                    points_to_b = True
                else:
                    points_to_b = False
                hospi_a, hospi_b = self.link_to_ab_hospi[link]
                hospi_dist = np.abs(hospi_a-hospi_b)
                if hospi_a < hospi_b:
                    hospi_b_is_larger = True
                else:
                    hospi_b_is_larger = False
                reward = - 1
                if points_to_b == hospi_b_is_larger:
                    reward = 1
                d_sum += reward*hospi_dist
                abs_d_sum += hospi_dist
            self.dag_to_gcf[dag] = d_sum/abs_d_sum

