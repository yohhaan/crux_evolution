from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns


def savefig(path, size=[4, 3]):
    import os
    import matplotlib
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.rcParams["figure.autolayout"] = True
    # Sane default fig size for papers
    matplotlib.rcParams["figure.figsize"] = [4, 3]

    # Uses Opentype-compatible fonts
    # conferences often require this for camera ready, so if you don't do it pre-submission you'll have a nightmare at camera-ready time.
    matplotlib.rcParams["pdf.fonttype"] = 42
    matplotlib.rcParams["ps.fonttype"] = 42

    # Automatically make the directory hierarchy so I can just save figures with path names
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Makes background transparent so plots can go in slides and look good
    plt.gcf().patch.set_alpha(0)
    # Default fig size
    plt.gcf().set_size_inches(*size)
    # Make figure fill whole PDF (otherwise figs have huge margins in LaTeX
    plt.tight_layout(
        pad=0,
    )
    plt.savefig(path, bbox_inches="tight")
    plt.clf()
    # Sets seaborn whitegrid on every plot for consistency (darkgrid is nice for slides)
    sns.set_style("whitegrid")


if __name__ == "__main__":
    # Create Argument Parser
    parser = argparse.ArgumentParser(
        prog="python3 heatmap.py",
        description="Heatmap visualization of stability of origins from top specified `rank` across time in CrUX",
    )
    parser.add_argument("crux_dir")
    parser.add_argument(
        "rank", type=int, choices=[1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    )
    args = parser.parse_args()

    crux_dir = args.crux_dir
    dfs = []
    filenames = []
    crux_size = 1000000
    crux_top = args.rank

    # collect filenames
    for filename in os.listdir(crux_dir):
        if filename.endswith(".csv"):
            filenames.append(filename)
    # sort in alphabetical order
    filenames = np.sort(filenames)
    # load each csv once
    for filename in filenames:
        df = pd.read_csv(os.path.join(crux_dir, filename))
        # assert len(df) == crux_size
        dfs.append(df[df["rank"] <= crux_top]["origin"].values)

    n = len(filenames)
    data = np.ones([n, n])
    for i in range(n):
        for j in range(n):
            if i == j:
                data[i][j] = len(dfs[i])
            else:
                # compute intersection
                intersection = len(set(dfs[i]).intersection(set(dfs[j])))
                data[i][j] = intersection
                data[j][i] = intersection

    # Hide lower triangle of results
    mask = np.tril(np.ones([n, n]), -1)
    labels = [os.path.splitext(filename)[0] for filename in filenames]
    df = pd.DataFrame(data, index=labels, columns=labels)
    # Heatmap, remove lower triangle
    sns.heatmap(
        data=df,
        mask=mask,
        xticklabels=4,
        yticklabels=4,
        annot=False,
        square=True,
    )
    plt.savefig("heatmap_" + str(crux_top) + ".png", bbox_inches="tight")  # for readme
    savefig("./heatmap_" + str(crux_top) + ".pdf")  # better quality
