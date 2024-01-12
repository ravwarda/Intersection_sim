import json
import numpy as np
import itertools


def generate_parmeters_file(filename="parameters.json", step=1):
    '''tworzy plik json z wszystkimi kombinacjami parametrów'''
    alpha = 1

    def normalize(x, min, max):
        return 2*alpha*(x - min) / (max - min) - alpha

    def denormalize(x, min, max):
        return (x + alpha) / (2*alpha) * (max - min) + min

    traffic_min = 1
    traffic_max = 20

    segment_min = 0.5
    segment_max = 1

    percentage_min = 0.25
    percentage_max = 0.5

    traffic_params = []
    segment_params = []
    percentage_params = []

    for i in np.arange(-alpha, alpha + step, step):
        traffic_params.append(denormalize(i, traffic_min, traffic_max))
        segment_params.append(denormalize(i, segment_min, segment_max))
        percentage_params.append(denormalize(
            i, percentage_min, percentage_max))

    all_combinations_list = list(itertools.product(
        *[traffic_params, segment_params, percentage_params]))  # tworzenie wszystkich kombinacji
    
    with open(filename, 'w') as f:
        f.write("[\n")
    for i in range(len(all_combinations_list)):
        dictionary = {
            'traffic': all_combinations_list[i][0],
            'segment': all_combinations_list[i][1],
            'percentage': all_combinations_list[i][2]
        }
        with open(filename, 'a') as f:
            json.dump(dictionary, f, indent=4)
            f.write(",\n")
            json.dump(dictionary, f, indent=4)
            f.write(",\n")
            json.dump(dictionary, f, indent=4)
            if i != len(all_combinations_list)-1:
                f.write(",\n")
    with open(filename, 'a') as f:
        f.write("\n]")


def get_parameters_from_file(filename="parameters.json"):
    '''pobiera parametry z pliku i zwraca listę słowników'''
    with open(filename) as f:
        data = json.load(f)
        return data
