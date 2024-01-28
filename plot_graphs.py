import matplotlib.pyplot as plt
import itertools
import math


class Graphs:
    def __init__(self, params) -> None:
        self.parameters = params

    def plot_graphs(self, intersection_times, roundabout_times):
        """funkcja obsługujące rysowanie różnych wykresów"""

        # self.plot_all_times(intersection_times, roundabout_times)

        aggregated_intersection_times = self.get_aggregated_n_times(
            intersection_times, 3
        )
        aggregated_roundabout_times = self.get_aggregated_n_times(roundabout_times, 3)

        self.plot_all_times(aggregated_intersection_times, aggregated_roundabout_times)

        for i in range(3):
            self.plot_aggregated_params(
                aggregated_intersection_times, aggregated_roundabout_times, i
            )

        for i in range(3):
            self.plot_for_all_params(
                aggregated_intersection_times, aggregated_roundabout_times, i
            )

    def get_aggregated_n_times(self, times, n=3):
        """funkcja bierze średnią z n kolejnych elementów listy i zwraca nową listę"""

        sum_3times = 0
        aggregated_times = []

        for index, time in enumerate(times):
            sum_3times += time
            if (index % n) == n - 1:
                aggregated_times.append(sum_3times / n)
                sum_3times = 0

        return aggregated_times

    def plot_all_times(self, int_times, rnd_times):
        """wypisuje wszystkie czasy dla każdego zestawu parametrów dla ronda i skrzyżowania"""

        plt.plot(int_times, "P", label="intersection", alpha=0.6)
        plt.plot(rnd_times, "ro", label="roundabout", alpha=0.6)
        plt.legend()
        plt.xlabel("data set")
        plt.ylabel("time")
        plt.title("Times for different data sets")
        plt.grid()
        plt.show()

    def plot_aggregated_params(self, int_times, rnd_times, which_parameter=0):
        """wypisuje średnie czasy dla zestawów parametrów z tym samym parametrem dla ronda i skrzyżowania"""

        def _calc_aggregated_times(step=9, offset=3):
            sums_int, sums_rnd = ([0, 0, 0], [0, 0, 0])
            repeat = offset
            for main_index in range(3):
                jump_index = 0
                counter = 0
                while jump_index < len(int_times):
                    for repeat_index in range(repeat):
                        if counter >= 9:
                            continue
                        sums_int[main_index] += int_times[
                            jump_index + repeat_index + main_index * offset
                        ]
                        sums_rnd[main_index] += rnd_times[
                            jump_index + repeat_index + main_index * offset
                        ]
                        counter += 1
                    jump_index += step
                    if counter >= 9:
                        continue

            agg_int_times = list(map(lambda x: x / 9, sums_int))
            agg_rnd_times = list(map(lambda x: x / 9, sums_rnd))

            return (agg_int_times, agg_rnd_times)

        aggregated_int_times, aggregated_rnd_times = (0, 0)
        name = None

        match which_parameter:
            case 0:
                # agregacja dla parametru traffic
                name = "traffic"
                aggregated_int_times, aggregated_rnd_times = _calc_aggregated_times(
                    step=1, offset=9
                )
            case 1:
                # agregacja dla parametru segment
                name = "segment"
                aggregated_int_times, aggregated_rnd_times = _calc_aggregated_times(
                    step=9, offset=3
                )
            case 2:
                # agregacja dla parametru percentage
                name = "percentage"
                aggregated_int_times, aggregated_rnd_times = _calc_aggregated_times(
                    step=3, offset=1
                )
            case _:
                raise Exception[
                    "Invalid which_parameter in plot_aggregated_params function"
                ]

        plt.plot(
            self.parameters[which_parameter],
            aggregated_int_times,
            "-P",
            label="intersection",
            alpha=0.6,
        )
        plt.plot(
            self.parameters[which_parameter],
            aggregated_rnd_times,
            "-ro",
            label="roundabout",
            alpha=0.6,
        )
        plt.legend()
        plt.xlabel(f"{name} parameter")
        plt.ylabel("average time")
        plt.title(f"Average times for data sets with the same {name} parameter")
        plt.grid()
        plt.show()

    def plot_for_all_params(self, int_times, rnd_times, which_parameter=0):
        def _get_times(step=9, offset=3):
            agg_int_times, agg_rnd_times = ([[], [], []], [[], [], []])
            repeat = offset
            for main_index in range(3):
                jump_index = 0
                counter = 0
                while jump_index < len(int_times):
                    for repeat_index in range(repeat):
                        if counter >= 9:
                            continue
                        agg_int_times[main_index].append(
                            int_times[jump_index + repeat_index + main_index * offset]
                        )
                        agg_rnd_times[main_index].append(
                            rnd_times[jump_index + repeat_index + main_index * offset]
                        )
                        counter += 1
                    jump_index += step
                    if counter >= 9:
                        continue

            return (agg_int_times, agg_rnd_times)

        aggregated_int_times, aggregated_rnd_times = (0, 0)
        name = None

        match which_parameter:
            case 0:
                # agregacja dla parametru traffic
                name = "traffic"
                aggregated_int_times, aggregated_rnd_times = _get_times(
                    step=1, offset=9
                )
            case 1:
                # agregacja dla parametru segment
                name = "segment"
                aggregated_int_times, aggregated_rnd_times = _get_times(
                    step=9, offset=3
                )
            case 2:
                # agregacja dla parametru percentage
                name = "percentage"
                aggregated_int_times, aggregated_rnd_times = _get_times(
                    step=3, offset=1
                )
            case _:
                raise Exception[
                    "Invalid which_parameter in plot_for_all_params function"
                ]

        figure, axis = plt.subplots(nrows=3, ncols=3, layout="constrained")

        for index in range(9):
            axis[math.floor(index / 3), index % 3].plot(
                self.parameters[which_parameter],
                [
                    aggregated_int_times[0][index],
                    aggregated_int_times[1][index],
                    aggregated_int_times[2][index],
                ],
                "-P",
                label="intersection",
                alpha=0.6,
            )
            axis[math.floor(index / 3), index % 3].plot(
                self.parameters[which_parameter],
                [
                    aggregated_rnd_times[0][index],
                    aggregated_rnd_times[1][index],
                    aggregated_rnd_times[2][index],
                ],
                "-ro",
                label="roundabout",
                alpha=0.6,
            )
            axis[math.floor(index / 3), index % 3].legend()
            axis[math.floor(index / 3), index % 3].grid()
            axis[math.floor(index / 3), index % 3].set_xlabel(f"{name} parameter")
            axis[math.floor(index / 3), index % 3].set_ylabel("average time")
            axis[math.floor(index / 3), index % 3].set_title(f"subplot {index}")
            figure.suptitle(f"Plots for the same {name} parameter", fontsize=16)
        plt.show()
