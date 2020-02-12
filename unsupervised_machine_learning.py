import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.cluster import MeanShift
from sklearn.datasets.samples_generator import make_blobs

style.use("ggplot")
from sklearn.cluster import KMeans

def kMeans():
    x = [1, 5, 1.5, 8, 1, 9]
    y = [2, 8, 1.8, 8, 0.6, 11]

    plt.scatter(x, y)
    plt.show()

    X = np.array([[1, 2],
                  [5, 8],
                  [1.5, 1.8],
                  [8, 8],
                  [1, 0.6],
                  [9, 11]])

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(X)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    print(centroids)
    print(labels)

    colors = ["g.", "r.", "c.", "y."]

    for i in range(len(X)):
        print("coordinate:", X[i], "label:", labels[i])
        plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)

    plt.scatter(centroids[:, 0], centroids[:, 1], marker="x", s=150, linewidths=5, zorder=10)

    plt.show()

def meanShift():
    centers = [[1, 1], [5, 5], [3, 10]]
    X, _ = make_blobs(n_samples=500, centers=centers, cluster_std=1)
    plt.scatter(X[:, 0], X[:, 1])


    plt.show()

    ms = MeanShift()


    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    print(cluster_centers)


    n_clusters_ = len(np.unique(labels))
    print("Number of estimated clusters:", n_clusters_)

    colors = 10 * ['r.', 'g.', 'b.', 'c.', 'k.', 'y.', 'm.']

    for i in range(len(X)):
        plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)


    plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1],
                marker="x", color='k', s=150, linewidths=5, zorder=10)

    plt.show()


meanShift()

