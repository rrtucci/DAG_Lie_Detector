from itertools import product
import numpy as np

class GCF_calculator:
    def __init__(self,
                 emp_probs,
                 links,
                 dag_list,
                 dag_to_link_directions):
        self.emp_probs = emp_probs
        self.links = links
        self.dag_list = dag_list
        self.dag_to_link_directions = dag_to_link_directions

        self.link_to_hospi_01 = {}
        self.dag_to_gcf = {}
        self.set_link_to_hospi_01()
        self.set_dag_to_gcf()

    def set_link_to_hospi_01(self):
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
            hospi_0 = 0
            hospi_1 = 0
            for k_0, k_1 in product(range(size_0), range(size_1)):
                x = prob_0[k_0]*prob_1[k_1]
                y_do_0 = np.log(prob_1[k_1]/prob_1_bar_do_0[k_0, k_1])
                y_do_1 = np.log(prob_0[k_0]/prob_0_bar_do_1[k_1, k_0])
                hospi_0 += x*y_do_0
                hospi_1 += x*y_do_1

            self.link_to_hospi_01[link] = [hospi_0, hospi_1]

    def set_dag_to_gcf(self):
        for dag in self.dag_list:
            d_sum = 0
            abs_d_sum = 0
            for k_link, link in enumerate(self.links):
                points_to_1 = \
                    (self.dag_to_link_directions[dag][k_link] == "0->1")
                hospi_0, hospi_1 = self.link_to_hospi_01[link]
                hospi_dist = np.abs(hospi_0-hospi_1)
                if hospi_0 < hospi_1:
                    hospi_1_is_larger = True
                else:
                    hospi_1_is_larger = False
                reward = - 1
                if points_to_1 == hospi_1_is_larger:
                    reward = 1
                d_sum += reward*hospi_dist
                abs_d_sum += hospi_dist
            self.dag_to_gcf[dag] = d_sum / max(abs_d_sum, 1e-10)

    def print_hospi_01(self):
        for link in self.links:
            hospi_0, hospi_1 = self.link_to_hospi_01[link]
            print("link", ", hospi_0", ", hospi_1")
            print(link,"\t", '%.5f'%hospi_0, "\t", '%.5f'%hospi_1)

    def print_GFCs(self):
        for dag, gcf in self.dag_to_gcf.items():
            print("dag=", dag.name, ",\tGCF=", "%.5f"%gcf)