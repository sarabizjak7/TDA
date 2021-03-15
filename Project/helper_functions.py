import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import gudhi

import numpy as np
np.random.seed(2)
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from scipy import stats

################################################################

def get_points_from_file(filename):
    # Prebere točke iz datoteke.
    points = []
    with open(filename, 'r') as data:
        for line in data:
            points.append(tuple(list(map(float, line.strip().split(' ')))))
    return points

def max_diameter(S):
    # Vrne premer množice točk S.
    D = pdist(np.array(S))
    D = squareform(D)
    return D.max()

def get_partition_points(R, parts):
    # Vrne seznam točk 0 = r_0 < r_1 < ... < r_parts < R dolžine parts+1.
    interval_size = R / parts
    return [i * interval_size for i in range(parts + 1)]

def construct_VR(points, partition_point, dim):
    # Konstruira drevo simpleksov dimenzije največ dim za Ripsov kompleks.
    VRi = gudhi.RipsComplex(points = points, max_edge_length = partition_point)
    tree_VRi = VRi.create_simplex_tree(max_dimension = dim)      
    return tree_VRi

def noise(eps):
    return eps * (2*np.random.rand()-1)

def add_noise_to_points(points):
    # Perturbira točke.
    dim = len(points[0])
    eps = max_diameter(points) / 100
    # na ta način bo največja evklidska razdalja med izvorno in zašumljeno točko res R/100
    eps = np.sqrt((eps**2)/3)
    points_noise = [tuple([p[i] + noise(eps) for i in range(dim)]) for p in points]
    return points_noise

def round_f_value(f_value, partition_points):
    # f_value navzdol zaokroži na najbližjo vrednost iz partition_points
    n = len(partition_points)
    f_value_int = f_value / partition_points[-1] * (n-1)
    f_value_int_floor = int(np.floor(f_value_int))
    if f_value_int_floor >= n:
        f_value_int_floor = n-1
    return partition_points[f_value_int_floor]

def make_simplex_tree_custom_filtration(points, partition_points=[], dim=3):
    # Naredimo drevo za Ripsov kompleks z največjim smiselnim parametrom,
    # nato filtracijsko vrednost za posamezni simpleks navzdol zaokrožimo na
    # najbližjo vrednost iz partitions_points.
    simplex_tree = construct_VR(points, 1.05*max_diameter(points), dim)
    if partition_points:
        for (simplex, f_value) in simplex_tree.get_simplices():
            f_value_new = round_f_value(f_value, partition_points)
            simplex_tree.assign_filtration(simplex, f_value_new)
    return simplex_tree

################################################################

def plot_points_and_diagrams(points, points_noise, dim, partition_points=None, max_intervals=1000):
    # narišemo točke (v 3d), zašumljene točke in diagram za vhodne točke
    # vztrajnostni diagram rišemo za simplekse dimenzije strogo manj kot dim
    # max_intervals pove, največ koliko intervalov (točk) bo narisal na graf
    x,y,z = [p[0] for p in points],[p[1] for p in points],[p[2] for p in points]
    x_n,y_n,z_n = [p[0] for p in points_noise],[p[1] for p in points_noise],[p[2] for p in points_noise]

    fig = plt.figure(figsize=(12,6))
    
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(x_n,y_n,z_n,c='red',label='perturbirane točke')
    ax1.scatter(x,y,z,c='blue',label='vhodne točke')
    
    ax1.set_title('Točke')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')
    ax1.legend()
    R = partition_points[-1] if partition_points else 1.05*max_diameter(points)

    simplex_tree = construct_VR(points, R, dim)
    simplex_tree.compute_persistence(persistence_dim_max=False)
    ax2 = fig.add_subplot(122)
    persistence = simplex_tree.persistence()
    gudhi.plot_persistence_diagram(persistence, max_intervals=max_intervals,
                                   axes=ax2, legend=True, fontsize=12)
    ax2.set_title('Vztrajnostni diagram za vhodne točke')

    fig.tight_layout(w_pad=2)
    plt.show()

def plot_normal_with_bottlenecks(bottlenecks_array, bottlenecks_mean, bottlenecks_std, epsilon=None, n_bins=40, combine_plots=True):    
    if combine_plots:
        fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(20,6))
        fig.suptitle('Histogram za razdalje bottleneck v dimenzijah 0, 1 in 2', fontsize=16)
        for plot_dim in range(3):
            mu = bottlenecks_mean[plot_dim]
            std = bottlenecks_std[plot_dim]
            bottlenecks_dim = bottlenecks_array[:,plot_dim]
            axs[plot_dim].hist(bottlenecks_dim, density=True,bins=n_bins, label='histogram v dimenziji {}'.format(plot_dim))
            x = np.linspace(mu-3*std, mu+3*std, 100)
            lab = 'N({},{})'.format(round(mu,2),round(std,2))
            axs[plot_dim].axvline(x = mu, color = 'r', label = 'avg(bottlenecks)') 
            if epsilon:
                axs[plot_dim].axvline(x = epsilon, color = 'g', label = 'epsilon') 
                axs[plot_dim].axvline(x = 2*epsilon, color = 'b', label = '2epsilon') 
            axs[plot_dim].plot(x, stats.norm.pdf(x, mu, std), label=lab)
            axs[plot_dim].set_xlabel('razdalja bottleneck')
            axs[plot_dim].set_ylabel('vrednost porazdelitvene funkcije')
            axs[plot_dim].set_title('Histogram za razdalje bottleneck v dimenziji {}'.format(plot_dim), fontsize=14)
            axs[plot_dim].legend()        
        plt.show()
    else:
        for plot_dim in range(3):
            mu = bottlenecks_mean[plot_dim]
            std = bottlenecks_std[plot_dim]
            bottlenecks_dim = bottlenecks_array[:,plot_dim]
            plt.hist(bottlenecks_dim, density=True,bins=40, label='histogram v dimenziji {}'.format(plot_dim))
            x = np.linspace(mu-3*std, mu+3*std, 100)
            lab = 'N({},{})'.format(round(mu,2),round(std,2))
            plt.axvline(x = mu, color = 'r', label = 'avg(bottlenecks)') 
            if epsilon:
                plt.axvline(x = epsilon, color = 'g', label = 'epsilon') 
                plt.axvline(x = 2*epsilon, color = 'b', label = '2epsilon') 
            plt.plot(x, stats.norm.pdf(x, mu, std), label=lab)
            plt.xlabel('razdalja bottleneck')
            plt.ylabel('vrednost porazdelitvene funkcije')
            plt.title('Histogram za razdalje bottleneck v dimenziji {}'.format(plot_dim), fontsize=14)
            plt.legend()
            plt.show()

################################################################    

def my_bottleneck_distance(simplex_tree, simplex_tree_noise):
    # izračuna bottleneck razdaljo med diagramoma dveh dreves za vsako dimenzijo posebej
    # seznam bottlenecks hrani na indeksu i razdaljo v dimenziji i
    bottlenecks = []
    simplex_tree.compute_persistence()
    simplex_tree_noise.compute_persistence()
    for i in range(3):
        persistence_diag = simplex_tree.persistence_intervals_in_dimension(i)
        persistence_diag_noise = simplex_tree_noise.persistence_intervals_in_dimension(i)
        bottlenecks.append(gudhi.bottleneck_distance(persistence_diag, persistence_diag_noise))
    return bottlenecks

def do_shapiro(bottlenecks_array):
    shapiro_stat_pValue = []
    for dim in range(3):
        shapiro_stat_pValue.append(stats.shapiro(bottlenecks_array[:,dim]))
    return np.array(shapiro_stat_pValue)
    
def do_statistics(points, n, partition_points=[], dim=3):
    # Izračuna n razdalj bottleneck za n neodvisnih perturbacij seznama točk points.
    # Če je podan seznam razdelilnih točk, jih upošteva, sicer naredi fino filtracijo z gudhijem.
    np.random.seed(n)
    simplex_tree = make_simplex_tree_custom_filtration(points, partition_points, dim)
    bottlenecks = []
    for i in range(n):
        print(i)
        points_noise = add_noise_to_points(points)
        simplex_tree_noise = make_simplex_tree_custom_filtration(points_noise, partition_points, dim)
        bottlenecks.append(my_bottleneck_distance(simplex_tree, simplex_tree_noise))
    return np.array(bottlenecks)