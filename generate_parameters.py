import json
import numpy as np
import itertools


class UseFile:
    def __init__(self):
        self.traffic_min = 2
        self.traffic_max = 16

        self.segment_min = 0.5
        self.segment_max = 1.2

        self.percentage_min = 0.25
        self.percentage_max = 0.45

        self.traffic_params = []
        self.segment_params = []
        self.percentage_params = []

    def generate_parmeters_file(self, filename="parameters.json", step=1):
        """tworzy plik json z wszystkimi kombinacjami parametrów x3"""
        alpha = 1

        def normalize(x, min, max):
            return 2 * alpha * (x - min) / (max - min) - alpha

        def denormalize(x, min, max):
            return (x + alpha) / (2 * alpha) * (max - min) + min

        for i in np.arange(-alpha, alpha + step, step):
            self.traffic_params.append(
                denormalize(i, self.traffic_min, self.traffic_max)
            )
            self.segment_params.append(
                denormalize(i, self.segment_min, self.segment_max)
            )
            self.percentage_params.append(
                denormalize(i, self.percentage_min, self.percentage_max)
            )

        all_combinations_list = list(
            itertools.product(
                *[self.traffic_params, self.segment_params, self.percentage_params]
            )
        )  # tworzenie wszystkich kombinacji parametrów

        with open(filename, "w") as f:
            f.write("[\n")
        for i in range(len(all_combinations_list)):
            dictionary = {
                "traffic": all_combinations_list[i][0],
                "segment": all_combinations_list[i][1],
                "percentage": all_combinations_list[i][2],
            }
            with open(filename, "a") as f:
                json.dump(dictionary, f, separators=(", ", ": "))
                f.write(",\n")
                json.dump(dictionary, f, separators=(", ", ": "))
                f.write(",\n")
                json.dump(dictionary, f, separators=(", ", ": "))
                if i != len(all_combinations_list) - 1:
                    f.write(",\n")
        with open(filename, "a") as f:
            f.write("\n]")

    def get_parameters_from_file(self, filename="parameters.json"):
        """pobiera parametry z pliku i zwraca listę słowników"""
        with open(filename) as f:
            data = json.load(f)
            return data

    def get_params(self):
        return (
            self.traffic_params.copy(),
            self.segment_params.copy(),
            self.percentage_params.copy(),
        )
