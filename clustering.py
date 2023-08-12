import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mc
from kmodes.kprototypes import KPrototypes

def kproto(cols, n_clusters=3):
    
    # Note that columns order should be ['Race', 'Gender', 'Age', 'Systolic', 'Total Cholesterol', 'HDL', 'Diabetes', 'Smoker', 'On hypertension treatment', 'ASCVD 10 Y Risk Score', 'Age', 'Gender', 'Smoking', 'Systolic', 'Diabetes', 'CAD', 'CVD', 'AAA', 'PAD', 'Time since last diagnosis', 'HDL', 'Total cholesterol', 'eGFR', 'hsCRP', 'SMART 10 Y Risk Score', 'Unmet Risk']
    subcols = [cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7], cols[8], cols[22], cols[23], cols[25]]
    subrows = np.transpose(subcols)
    
    # We need to define the categorical (versus numeric) columns for KPrototypes
    # categorical = [ race, gender, diabetes, smoker, on_hypertension_treatment]
    # categorical = [    0,      1,        6,      7,                         8]
    cluster_labels = KPrototypes(n_clusters=n_clusters).fit_predict(subrows, categorical=[0, 1, 6, 7, 8])
    return cluster_labels

def plot_cluster(x, y, cluster_labels, plot_x_label='ASCVD', plot_y_label='UMRI'):
    x = list(map(float, x))
    y = list(map(float, y))
    markersizes = [1 for i in x]

    # Randomize cluster colours selection
    if len(set(cluster_labels)) > 10:
        colors = list(mc.CSS4_COLORS.keys())
        random.shuffle(colors)
        colors = colors[:len(set(cluster_labels))]
    elif len(set(cluster_labels)) == 1:
        colors = ['tab:red']
    else:
        colors = list(mc.TABLEAU_COLORS.keys())
        random.shuffle(colors)
        colors = colors[:len(set(cluster_labels))]

    # Plot the figure with colour bar
    fig = plt.figure(figsize=(8,8))
    plt.scatter(x, y, s=markersizes, c=cluster_labels, cmap=mc.ListedColormap(colors))
    plt.xlim(-0.01, 1)
    plt.ylim(-0.01, 100)
    if len(set(cluster_labels)) > 1:
        cb = plt.colorbar()
        cb.set_ticks( np.arange(0, max(cluster_labels), max(cluster_labels)/float(len(colors))) )
        cb.set_ticklabels(colors)

    plt.xlabel = plot_x_label
    plt.ylabel = plot_y_label
    plt.show()
