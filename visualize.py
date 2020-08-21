"""
Python module to create visulalizations for the different empirical tests.
"""
import math
import matplotlib.pyplot as plt
import numpy as np


def main():
    # visualize_random_walk()
    # visualize_sac_test()
    #visualize_sts_results("Ascon-128", "AlgorithmTesting_Ascon128/")
    visualize_sts_results("Ascon-128a", "AlgorithmTesting_Ascon128a/")
    visualize_sts_results("Isap-A-128a", "AlgorithmTesting_isap_a/")
    visualize_sts_results("Isap-K-128a", "AlgorithmTesting_isap_k/")
    visualize_sts_results("Oribatida-256-64", "AlgorithmTesting_Oribatida/")
    visualize_sts_results("LOTUS-AEAD-64", "AlgorithmTesting_lotus/")
    visualize_sts_results("LOCUS-AEAD-64", "AlgorithmTesting_locus/")
    visualize_sts_results("SpoC-128s", "AlgorithmTesting_spoc/")
    #visualize_sts_results("Calibration", "sts-2.1.2/experiments/AlgorithmTesting/")
    # Ascon-128, Ascon-128a, Isap-A-128a, Isap-K-128a, SpoC-128s, Oribatida-256-64, LOTUS-AEAD-64, LOCUS-AEAD-64


def visualize_sac_test():
    """
    Creates one general Plot about passing P-Values and several Histograms of each algorithm.
    """
    with open("sac_results.txt") as file:
        data = []
        alg_counts = []
        file.readline()
        title = "Ascon-128"
        algorithms = ["Ascon-128"]
        for _ in range(0, 86023):
            temp = file.readline()
            if 'encryption' in temp:
                plt.hist(data, bins=[0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
                                     0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0], align="mid")
                best_fit = len(data) / 20
                plt.plot([0.0, 1.0], [best_fit, best_fit], ':r')
                plt.ylabel("Frequency Count")
                plt.xlabel("Sub-Intervals")
                plt.xticks(np.arange(0, 1.05, step=0.05))
                plt.title("SAC Test for " + title.capitalize())
                plt.xticks(rotation=45)
                plt.savefig("plots/SAC-" + title.capitalize(),
                            dpi=350, bbox_inches='tight')
                plt.clf()
                count = len([i for i in data if i > 0.01]) / len(data)
                print(count)
                alg_counts.append(count)
                title = temp[22:-3]
                algorithms.append(title[:-1].capitalize())
                data.clear()
            else:
                data.append(float(temp))
        plt.hist(data, bins=[0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
                             0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0], align="mid")
        best_fit = len(data) / 20
        plt.plot([0.0, 1.0], [best_fit, best_fit], ':r')
        plt.ylabel("Frequency Count")
        plt.xlabel("Sub-Intervals")
        plt.xticks(np.arange(0, 1.05, step=0.05))
        plt.title("SAC Test for " + title.capitalize())
        plt.xticks(rotation=45)
        plt.savefig("plots/SAC-" + title.capitalize(),
                    dpi=350, bbox_inches='tight')
        plt.clf()
        count = len([i for i in data if i > 0.01]) / len(data)
        alg_counts.append(count)
        print(alg_counts)
        confidence_min = 0.99-3*math.sqrt(0.99*0.01/32768)
        confidence_maxis = 0.99+3*math.sqrt(0.99*0.01/32768)
        plt.scatter(algorithms, alg_counts)
        xmin, xmaxis = plt.xlim()
        plt.style.use("ggplot")
        plt.fill_between([xmin, xmaxis], confidence_min,
                         confidence_maxis, alpha=0.05, color='gray')
        plt.title("Proportion of passing p-Values")
        plt.plot([xmin, xmaxis], [confidence_maxis, confidence_maxis],
                 ':r', label='Confidence Intervall')
        plt.plot([xmin, xmaxis], [confidence_min, confidence_min], ':r')
        plt.plot([xmin, xmaxis], [0.99, 0.99], '-', label='1-\u03B1 = 0.99')
        plt.xlabel("Algorithms")
        plt.ylabel("Proportions")
        plt.xticks(rotation=45)
        plt.legend(loc="upper right")
        plt.savefig("plots/SAC-Passing", dpi=450, bbox_inches='tight')


def visualize_sts_results(algorithm, path):
    """
    Creates the different plots for the results of the STS.

    Args:
        algorithm (String): The Name of the examined Algorithm.
        path (String): Path to the saved results for the algorithm.
    """
    test_paths = ["Frequency", "BlockFrequency", "Runs", "LongestRun", "Rank", "FFT", "NonOverlappingTemplate", "OverlappingTemplate",
                  "Universal", "LinearComplexity", "Serial", "ApproximateEntropy", "CumulativeSums", "RandomExcursions", "RandomExcursionsVariant"]
    test_names = ["Frequency", "Block Frequency", "Runs", "Longest Run", "Rank", "Spectral Test", "Non-Overlapping Template", "Overlapping Template",
                  "Universal", "Linear Complexity", "Serial", "Approximate Entropy", "Cumulative Sums", "Random Excursions", "Random Excursions Variant"]
    test_counts = []

    for index in range(0, 15):
        with open(path + test_paths[index] + "/results.txt") as file:
            data = file.read().splitlines()
            data = [float(i) for i in data]
            data = list(filter(lambda x: x != 0.000000, data))
            count = len([i for i in data if i > 0.01]) / len(data)
            test_counts.append(count)
            best_fit = len(data) / 20
            plt.hist(data, bins=[0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35,
                                 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0])
            plt.plot([0.0, 1.0], [best_fit, best_fit], ':r')
            plt.title(test_names[index])
            plt.xlabel("Sub-Intervalls")
            plt.ylabel("Frequency Count")

            plt.savefig("plots/" + algorithm + "/sts-histogramm-" +
                        algorithm + test_names[index], dpi=100, bbox_inches='tight')
            plt.clf()

    plt.figure(figsize=(13, 10))
    confidence_min = 0.99-3*math.sqrt(0.99*0.01/1040)
    confidence_maxis = 0.99+3*math.sqrt(0.99*0.01/1040)
    plt.scatter(test_names, test_counts)
    xmin, xmaxis = plt.xlim()
    plt.fill_between([xmin, xmaxis], confidence_min,
                     confidence_maxis, alpha=0.05, color='gray')
    plt.plot([xmin, xmaxis], [confidence_maxis, confidence_maxis],
             ':r', label='Confidence Intervall')
    plt.plot([xmin, xmaxis], [0.99, 0.99], '-', label='1-\u03B1 = 0.99')
    plt.plot([xmin, xmaxis], [confidence_min, confidence_min], ':r')
    plt.xticks(rotation=45, ha="right", fontsize=14)
    plt.title("Proportion of passing P-Values", fontsize=18)
    plt.xlabel("Tests", fontsize=16)
    plt.ylabel("Proportions", fontsize=16)
    plt.legend(loc="upper right")
    plt.savefig("plots/" + algorithm + "/sts-Passing" +
                algorithm, dpi=450, bbox_inches='tight')
    plt.clf()

    nonoverlapping_proportions = []
    for index in range(1, 149):
        with open(path + "NonOverlappingTemplate" + "/data" + str(index) + ".txt") as file:
            temp_data = file.read().splitlines()
            temp_data = [float(i) for i in temp_data]
            temp_data = list(filter(lambda x: x != 0.000000, temp_data))
            proportion = len(
                [i for i in temp_data if i > 0.01]) / len(temp_data)
            nonoverlapping_proportions.append(proportion)
    print(nonoverlapping_proportions)
    print(len(nonoverlapping_proportions))
    plt.figure(figsize=(10, 10))
    plt.hist(nonoverlapping_proportions)
    ymin, ymaxis = plt.ylim()
    plt.plot([confidence_min, confidence_min], [ymin, ymaxis],
             ':r', label='Confidence Intervall')
    plt.plot([0.99, 0.99], [ymin, ymaxis], '-', label='1-\u03B1 = 0.99')
    plt.plot([confidence_maxis, confidence_maxis], [ymin, ymaxis], ':r')
    plt.title(
        "Proportion of passing P-Values of Non-Overlapping Template Test", fontsize=18)
    plt.xlabel("Proportion", fontsize=15)
    plt.ylabel("Frequency Count", fontsize=15)
    plt.savefig("plots/" + algorithm + "/sts-Non-Overlapping-" +
                algorithm, dpi=450, bbox_inches='tight')
    plt.clf()


if __name__ == "__main__":
    main()
