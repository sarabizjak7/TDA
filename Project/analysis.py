from operator import add
from helper_functions import *
import pickle
from multiprocessing import Pool
from scipy import stats


################################################################

# Branje točk
filename = 'persistence02_100'
filepath = 'persistence/' + filename + '.out'
points = get_points_from_file(filepath)
points = points[:]

################################################################

# RISANJE

if True:
    R = max_diameter(points) * 1.05
    partition_points = get_partition_points(R, 10)
    points_noise = add_noise_to_points(points)
    # narišemo točke, zašumljene točke in diagrama za obe drevesi
    plot_points_and_diagrams(points, points_noise, 
                            3, partition_points=[], max_intervals=1000)

################################################################

# RAČUNANJE BOTTLENECK IN STATISTIKA

R = max_diameter(points) * 1.05
partition_points = []
#partition_points = get_partition_points(max_diameter(points)*1.05, 10)

# razdelitve za paralelno računanje
paralist100_4 = [24,26,23,27]
paralist1000_4 = [252,248,251,249]
paralist1000_6 = [169,166,165,170,167,163]
paralist1000_12 = [79,81,78,82,77,83,76,84,75,85,99,101]
paralist = paralist1000_4

# ti dve funkciji uporabimo za paralelno računanje spodaj
def do_statistics_parallel(n):
    return do_statistics(points, n)

def do_statistics_part_points_parallel(n):
    return do_statistics(points, n, partition_points=partition_points)

if __name__ == '__main__':
    # množimo z 1.05, da polovimo tudi vse zašumljene točke
    compute = False
    plot = False
    if compute:
        with Pool(len(paralist)) as p:
            b = p.map(do_statistics_parallel, paralist)
            #b = p.map(do_statistics_part_points_parallel, paralist)
        
        bottlenecks_array = np.vstack(tuple(b))
        bottlenecks_mean = np.mean(bottlenecks_array, axis=0)
        bottlenecks_std = np.std(bottlenecks_array, axis=0)

        # Shranjevanje v datoteko
        str_num_part_points = str(len(partition_points)) if partition_points else 'inf'
        new_filename = 'pickle/' + filename + '_pp' + str_num_part_points + '_samples' + str(sum(paralist)) + '.pkl'
        with open(new_filename, 'wb') as f:
            print('Shranjujem v: ' + new_filename)
            point_cloud_results_to_pickle = [filepath, points, bottlenecks_array, bottlenecks_mean, bottlenecks_std]
            pickle.dump(point_cloud_results_to_pickle, f)
        
    # Branje
    if not compute and plot:
        str_num_part_points = str(len(partition_points)) if partition_points else 'inf'
        new_filename = 'pickle/' + filename + '_pp' + str_num_part_points + '_samples' + str(sum(paralist)) + '.pkl'
        with open(new_filename, 'rb') as f:
            filepath, points, bottlenecks_array, bottlenecks_mean, bottlenecks_std = pickle.load(f)
            print(bottlenecks_array)
            print('R:',max_diameter(points))
            print(np.max(bottlenecks_array,axis=0))
            plot_normal_with_bottlenecks(bottlenecks_array, bottlenecks_mean, bottlenecks_std, max_diameter(points)/100)

            print('Shapiro: (statistika, p-vrednost)')
            shapiro_stat_pValue = do_shapiro(bottlenecks_array)
            print(shapiro_stat_pValue)
