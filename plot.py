import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

sfmt = matplotlib.ticker.ScalarFormatter(useMathText=True)
sfmt.set_powerlimits((0, 0))
font = {'family': 'serif', 'size': 6}
matplotlib.rc('font', **font)

def input_data(filenames):

    info = {}
    for file in filenames:

        info[file] = {"n": set()}

        with open(os.path.join('logs/', file)) as f:
            for content in f.readlines():
                line = content.rstrip().split(' ')

                n = int(line[0])
                run_time = float(line[1])
                memory = float(line[2])

                if not (run_time, memory) == (-1.0, -1.0):

                    info[file]["n"].add(n)
                    info[file][n]  = (run_time, memory/(1024))

        info[file]["n"] = np.sort(list(info[file]["n"]))

    return info


if __name__ == '__main__':

    filenames = ['devito-rtm.txt',
                 'torch-rtm.txt']

    info = input_data(filenames)

    colors = [(0.0,0.0,0.0),
              (0.0,0.584,1.0),
              (1.0,0.0,0.286),
              (0.0,0.584,0.239),
              '#c2c22f',
              '#737373',
              '#a1c0ff',
              '#6b9cff',
              '#91eda2',
              '#ffff61']

    if not os.path.exists('fancy-figs/'):
        os.mkdir('fancy-figs/')

    # from IPython import embed; embed()
    # Plot wall-clock time
    fig, ax = plt.subplots(figsize=(3, 6))

    for j, file in enumerate(info.keys()):
        run_times = []
        n_list = []
        for n in info[file]["n"]:
            if (n) in info[file].keys():
                run_times.append(info[file][n][0])
                n_list.append(n)

        if j == 1:
            linestyle = '--'
            marker = 'v'
        else:
            linestyle = '-'
            marker = 'o'

        ax.plot(n_list, run_times, color=colors[j],
                    linewidth=0.4, linestyle=linestyle, marker=marker, ms=1,
                    label=(file[:file.find('-')]))

        ax.legend(fontsize=7, ncol=1, loc='upper left')
        ax.set_ylabel("Wall-clock time (s)", fontsize=8)
        ax.set_xlabel(r"$n$", fontsize=10)
        # ax.set_title(r"$50$ calls to "
        #                  + r"$3 \times 3 \ conv$"
        #                  + " — image size: "
        #                  + r"$n \times n \times n_c$")
        # ax.set_title("image size: "
        #              + r"$n \times n \times n_c$")
        # ax.set_xscale('log')
        # ax.set_yscale('log')
        # ax.set_xlim([1e2, 2e4])
        # ax.set_ylim([3e-1, 4e2])
        ax.grid(True, which="both", ls="-", alpha=.2)

    fig.savefig(os.path.join('fancy-figs/', 'runtime.png'),
                format='png', bbox_inches='tight',
                dpi=600, pad_inches=.05)
    plt.close(fig)


    # Plot peak memory usage
    fig, ax = plt.subplots(figsize=(3, 6))

    for j, file in enumerate(info.keys()):
        run_times = []
        n_list = []
        for n in info[file]["n"]:
            if (n) in info[file].keys():
                run_times.append(info[file][n][1])
                n_list.append(n)

        if j == 1:
            linestyle = '--'
            marker = 'v'
        else:
            linestyle = '-'
            marker = 'o'

        ax.plot(n_list, run_times, color=colors[j],
                    linewidth=0.4, linestyle=linestyle, marker=marker, ms=1,
                    label=(file[:file.find('-')]))

        ax.legend(fontsize=7, ncol=1, loc='upper left')
        ax.set_ylabel("Memory (MB)", fontsize=8)
        ax.set_xlabel(r"$n$", fontsize=10)
        # ax.set_title(r"$50$ calls to "
        #                  + r"$3 \times 3 \ conv$"
        #                  + " — image size: "
        #                  + r"$n \times n \times n_c$")
        # ax.set_title("image size: "
        #              + r"$n \times n \times n_c$")
        # ax.set_xscale('log')
        # ax.set_yscale('log')
        # ax.set_xlim([1e2, 2e4])
        # ax.set_ylim([3e-1, 4e2])
        ax.grid(True, which="both", ls="-", alpha=.2)


    fig.savefig(os.path.join('fancy-figs/', 'memory.png'),
                format='png', bbox_inches='tight',
                dpi=600, pad_inches=.05)
    plt.close(fig)
