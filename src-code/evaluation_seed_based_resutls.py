import networkx as nx
from Utils import *
import os
import matplotlib.pyplot as plt

########### Test result evaluation
print("################# SB De-anonymization Rate #####################")
try:
    path = '../evaluation/seed_based_test_result/'

    files = os.listdir(path)
    mapping_rates = []
    thetas = []
    for filename in files:
        temp = filename.split("_")[1].split(".")
        theta_str = "".join((temp[0], ".", temp[1]))
        theta = float(theta_str)

        # loading the test graphs G1 and G2

        G1 = nx.read_edgelist('input/G1.edgelist', comments='#', delimiter=' ',
                              create_using=nx.DiGraph(), nodetype=int)

        G2 = nx.read_edgelist('input/G2.edgelist', comments='#', delimiter=' ',
                              create_using=nx.DiGraph(), nodetype=int)

        # now check which left nodes are in the G1 and which right nodes are in the G2
        left_seeds = Utils.read_column("".join((path, filename)), 0)
        right_seeds = Utils.read_column("".join((path, filename)), 1)
        found_node_count_G1 = 0
        found_node_count_G2 = 0
        for seed_node in left_seeds:
            if G1.has_node(seed_node):
                found_node_count_G1 += 1

        for seed_node in right_seeds:
            if G2.has_node(seed_node):
                found_node_count_G2 += 1
        # found_left_node_count + found_right_node_count over total node(G1+G2) is the mapping rate
        total_mapped_nodes = found_node_count_G1 + found_node_count_G2
        total_node_test_dataset = len(G1.nodes) + len(G2.nodes)

        de_anony_rate = (total_mapped_nodes / total_node_test_dataset) * 100
        print("SB DA Rate : ", format(de_anony_rate, '.2f'), " % ", "for THETA: ", theta)
        thetas.append(theta)
        mapping_rates.append(de_anony_rate)

    # mapping_rates = [95, 93.4, 93, 92, 92, 91, 93]
    # thetas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    plt.plot(thetas, mapping_rates, color='red', marker='o',
             linestyle='solid', linewidth=2, markersize=12)
    plt.axis([0, 0.9, 90, 100])
    # plt.xticks(thetas)
    # plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.xlabel(r'$\theta$')
    plt.ylabel('Seed Based DA Rate(%)')
    plt.savefig("../evaluation/plot/seed_based_mapping_rate.png")
    # plt.grid()
    plt.show()

except Exception as e:
    print(e)



########### Validation result evaluation
print("############## SB De-anonymization Accuracy #######################")
try:
    path = '../evaluation/seed_based_validation_result/'
    files = os.listdir(path)
    accuracies = []
    thetas = []
    for filename in files:
        temp = filename.split("_")[1].split(".")
        theta_str = "".join((temp[0], ".", temp[1]))
        theta = float(theta_str)
        thetas.append(theta)
        # loading resultant mapping
        resultant_mapping = nx.read_edgelist("".join((path, filename)),
                                                create_using=nx.Graph(),
                                                comments='#', delimiter = ' ', nodetype=int)

        # loading validation mapping [Ground Truth(GT)]
        gt_mapping = nx.read_edgelist('input/validation_seed_mapping.txt',
                                        create_using=nx.Graph(),
                                        comments='#', delimiter=' ', nodetype=int)

        diff = nx.Graph()
        match_cnt = 0
        for edge in resultant_mapping.edges:
            try:
                if gt_mapping.has_edge(edge[0], edge[1]):
                    diff.add_edge(edge[0], edge[1])
                    match_cnt += 1
            except KeyError as e:
                print("No node of value: ", edge[0])

        de_anony_accuracy = (match_cnt / len(gt_mapping.edges)) * 100
        # print("match_cnt : ", match_cnt)
        print("SB DA Accuracy : ", de_anony_accuracy, " % ", "for THETA: ", theta)
        accuracies.append(de_anony_accuracy)

    plt.plot(thetas, accuracies, color='red', marker='o',
             linestyle='solid', linewidth=2, markersize=12)
    plt.axis([0, 1, 50, 100])
    # plt.xticks(thetas)
    # plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.xlabel(r'$\theta$')
    plt.ylabel('Seed based DA Accuracy(%)')
    # plt.grid()
    plt.savefig("../evaluation/plot/seed_based_accuracies.png")
    plt.show()
except Exception as e:
    print(e)


