import os
import matplotlib.pyplot as plt
import numpy as np

from event import Event
from intersection import Intersection
from simulation import Simulation
from roundabout import rondo_run_sim
from generate_parameters import *


def simulations_from_file(
    parameters, generate_new_file=False, filename="parameters.json"
):
    """wielokrotnie wywołuje symulacje dla wszystkich zestawów parametrów z pliku"""
    if (not os.path.isfile(filename)) or generate_new_file:
        generate_parmeters_file(filename)
    parameters_list = get_parameters_from_file(filename)
    intersection_times = []
    roundabout_times = []
    for parmeters_dict in parameters_list:
        parameters[2] = parmeters_dict["traffic"]
        parameters[3] = parmeters_dict["segment"]
        parameters[4] = parmeters_dict["percentage"]

        cars_out_intersection, cars_out_rnd = sim_call(parameters)

        intersection_times.append(calculate_sim_time(cars_out_intersection))
        roundabout_times.append(calculate_sim_time(cars_out_rnd))

    make_chart(intersection_times, roundabout_times)


def calculate_sim_time(cars_out_list):
    """zlicza średni czasu przejazdu dla aut w symulacji"""
    if len(cars_out_list[0]) == 0:
        return -10

    times_in_sim = []

    for i in range(0, len(cars_out_list[0])):
        times_in_sim.append(cars_out_list[1][i] - cars_out_list[0][i].arrival_time)

    return np.average(times_in_sim)


def sim_call(parameters, summary=False):
    """pojedyczne wywołanie symulacji dla jednego zestawu parametrów"""
    (
        sim_time,
        warm_up_time,
        traffic_intensity,
        segment_drive_time_distribution,
        percentage_cars_on_main_road,
        force_intensity,
        starting_drive_time_distribution,
    ) = parameters

    sim = Simulation(
        sim_time,
        warm_up_time,
        traffic_intensity,
        segment_drive_time_distribution,
        percentage_cars_on_main_road,
        force_intensity,
        starting_drive_time_distribution,
    )

    sim.generate_cars_list()
    cars_list = sim.get_cars_list()

    events_list = []
    for car in cars_list:
        events_list.append(Event(car))

    cars_out_intersection = Intersection(events_list).run_sim(
        sim_time, warm_up_time, describe=False
    )

    cars_out_rnd = rondo_run_sim(sim.get_cars_list(), sim_time, warm_up_time)

    if summary:
        sim_summary(cars_out_intersection, "Intersection", extended_summary=True)
        sim_summary(cars_out_rnd, "Roundabout", extended_summary=True)

    return cars_out_intersection, cars_out_rnd


def sim_summary(cars_out_list, name=None, extended_summary=False):
    """wypisanie przebiegu symulacji"""
    print("_" * 80)
    print(f"\n---{name}---\n")
    for i in range(0, len(cars_out_list[0])):
        print(i + 1, end=". ")
        if extended_summary:
            print(cars_out_list[0][i].arrival_time, end=" ")
            print(cars_out_list[0][i].entry_direction, end="--->")
            print(cars_out_list[0][i].destination_direction, end=" ")
            print(cars_out_list[0][i].segment_drive_time, end=" ")
        print(
            f"Czas przejazdu auta: {cars_out_list[1][i] - cars_out_list[0][i].arrival_time}"
        )
    print(f"\nIle aut przejechało w symulacji: {len(cars_out_list[0])}\n")
    print(
        "Sprawność {} wynosi: {}\n".format(
            "ronda" if name == "Roundabout" else "skrzyżowania",
            calculate_sim_time(cars_out_list),
        )
    )
    # print("Ile aut razem (sym + w czasie rozgrzewania): {}".format(len(cars_list)))


def make_chart(int_times, rnd_times):
    plt.plot(int_times, "P", label="intersection", alpha=0.6)
    plt.plot(rnd_times, "ro", label="roundabout", alpha=0.6)
    plt.legend()
    plt.xlabel("data sets")
    plt.ylabel("time")
    plt.grid()
    plt.show()
