import matplotlib.pyplot as plt


def plot_graphs(intersection_times, roundabout_times):
    """funkcja obsługujące rysowanie różnych wykresów"""

    # plot_all_times(intersection_times, roundabout_times)

    aggregated_intersection_times = aggregate_n_times(intersection_times, 3)
    aggregated_roundabout_times = aggregate_n_times(roundabout_times, 3)

    plot_all_times(aggregated_intersection_times, aggregated_roundabout_times)

    plot_aggregated_params_for_traffic(
        aggregated_intersection_times, aggregated_roundabout_times
    )


def aggregate_n_times(times, n=3):
    """funkcja bierze średnią z n kolejnych elementów listy i zwraca nową listę"""

    sum_3times = 0
    aggregated_times = []

    for index, time in enumerate(times):
        sum_3times += time
        if (index % n) == n - 1:
            aggregated_times.append(sum_3times / n)
            sum_3times = 0

    return aggregated_times


def plot_all_times(int_times, rnd_times):
    """wypisuje wszystkie czasy dla każdego zestawu parametrów dla ronda i skrzyżowania"""

    plt.plot(int_times, "P", label="intersection", alpha=0.6)
    plt.plot(rnd_times, "ro", label="roundabout", alpha=0.6)
    plt.legend()
    plt.xlabel("data set")
    plt.ylabel("time")
    plt.title("Times for different data sets")
    plt.grid()
    plt.show()


def plot_aggregated_params_for_traffic(int_times, rnd_times):
    """wypisuje średnie czasy dla zestawów parametrów z tym samym parametrem traffic dla ronda i skrzyżowania"""

    aggregated_int_times = aggregate_n_times(int_times, 9)
    aggregated_rnd_times = aggregate_n_times(rnd_times, 9)

    plt.plot([2, 9, 16], aggregated_int_times, "-P", label="intersection", alpha=0.6)
    plt.plot([2, 9, 16], aggregated_rnd_times, "-ro", label="roundabout", alpha=0.6)
    plt.legend()
    plt.xlabel("traffic intensity")
    plt.ylabel("average time")
    plt.title("Average times for data sets with the same traffic intesity")
    plt.grid()
    plt.show()
