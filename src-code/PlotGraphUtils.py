import matplotlib as plt

class PlotGraphUtils:


    @staticmethod
    def draw(in_values, out_values, in_hist, out_hist):
        plt.figure()  # you need to first do 'import pylab as plt'
        plt.grid(True)
        plt.plot(in_values, in_hist, 'ro-')  # in-degree
        plt.plot(out_values, out_hist, 'bv-')  # out-degree
        plt.legend(['In-degree', 'Out-degree'])
        plt.xlabel('Degree')
        plt.ylabel('Number of nodes')
        plt.title('network of places in Cambridge')
        plt.xlim([0, 2 * 10 ** 2])
        plt.savefig('./output/cam_net_degree_distribution.pdf')
        plt.close()