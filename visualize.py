import os
import matplotlib.pyplot as plt
import numpy as np


def main():
    #visualize_random_walk()
    visualize_sts_results()
    #visualize_single_result("sts-2.1.2/experiments/AlgorithmTesting/LongestRun/results.txt")


def visualize_sts_results():
    experiments = [f.path for f in os.scandir("sts-2.1.2/experiments/AlgorithmTesting/") if f.is_dir()]
    fig, axes = plt.subplots(5, 3, figsize=(25, 12.5), dpi=75, sharex=True, sharey=True)
    colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:pink', 'tab:olive', 'tab:red', 'tab:blue', 'tab:green', 'tab:pink', 'tab:olive', 'tab:red', 'tab:blue', 'tab:green', 'tab:pink', 'tab:olive']
    axes.flatten()
    bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    plt.style.use('fivethirtyeight')
    for index, test in enumerate(experiments):
        result = open(str(test) + "/results.txt", "r")
        data = result.readlines()
        print(test)
        print(len(data))
        for index1, entry in enumerate(data):
            data[index1] = truncate(entry, 1)
        print(data)
        data.sort()
        converted_list = [float(i) for i in data]
        print(converted_list)
        print(type(converted_list[0]))
        if index >= 5 and index < 10:
            ax = axes[index - 5, 1]
            ax.hist(converted_list, bins=bins, align='mid', label=str(test), color=colors[index])
            ax.set_title(test)
        elif index >= 10:
            ax = axes[index - 10, 2]
            ax.hist(converted_list, label=str(test), color=colors[index])
            ax.set_title(test)
        else:
            ax = axes[index, 0]
            ax.hist(converted_list, label=str(test), color=colors[index])
            ax.set_title(test)
    plt.suptitle("Grand Test", y=1.05, size=16)
    plt.tight_layout()
    plt.show()
    """
    plt.hist(data, density=True, bins=30, label="Data")
    mn, mx = plt.xlim()
    plt.xlim(mn, mx)
    plt.legend(loc="upper left")
    plt.ylabel('Probability')
    plt.xlabel('Data')
    plt.title("Histogram")
    plt.savefig("Histogramm", dpi=250)
    plt.clf()
    """
    fig.show()    
    
def visualize_single_result(path_to_result):
    result = open(path_to_result)
    data = np.array(result.readlines()).astype(np.float)
    #for index, entry in enumerate(data):
    #    data[index] = truncate(entry, 1)
    hist, bin_edges = np.histogram(data)
    print(hist)
    print(bin_edges)
    # The leftmost and rightmost bin edges
    first_edge, last_edge = data.min(), data.max()

    n_equal_bins = 10  # NumPy's default
    bin_edges = np.linspace(start=first_edge, stop=last_edge, num=n_equal_bins + 1, endpoint=True)

    print(bin_edges)

    #values, counts = np.unique(data, return_counts=True)
    #hist, _ = np.histogram(data, range=(0, data.max()), bins=data.max() + 1)

    #np.array_equal(hist, counts)


    # Reproducing `collections.Counter`
    #dict(zip(np.unique(data), counts[counts.nonzero()]))




    plot = plt.hist(data, density=True, bins=50, label="Data")
    plot
    plot.xlim(0.1, 1.0)
    plot.legend(loc="upper left")
    plot.ylabel('Frequeny Counts')
    plot.xlabel('P-Values')
    plot.title("Histogram")
    plt.savefig("plots/Histogramm", dpi=250)
    plt.clf()

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def visualize_random_walk():
    """
    Generate Random Walk Chart from ciphertext.

    Args:
        cipher ([Char]): Generated cipher that will be visualized in an one-dimensional chart.
    """
    data = []
    origin = 0
    position = 1
    data.append(origin)
    with open('sts-2.1.2/data/cipher-isap_a_c_1000000.txt') as file:
        while True:
            char = file.read(1)
            if not char:
                break
            if char == '1':
                origin = origin + 1
            elif char == '0':
                origin = origin - 1
            position = position+1
            data.append(origin)
    fig = plt.figure(figsize=(8,4), dpi=200)
    axis = fig.add_subplot(111)
    axis.scatter(np.arange(len(data)), data, c='blue', alpha=0.25, s=0.05)
    axis.plot(data, c='blue', alpha=0.5, lw=0.5, ls='-',)
    axis.plot(0, data[:1], c='red', marker='+')
    axis.axhline(linewidth=1, color='gray')
    plt.title('Random Walk of Isap Variant A with N=8.000.000')
    plt.tight_layout(pad=0)
    plt.savefig('plots/random_walk_1d.png', dpi=250)

if __name__ == "__main__":
    main()
