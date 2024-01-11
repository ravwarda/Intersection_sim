import matplotlib.pyplot as plt
from intersection import Intersection
from event import Event
from simulation import Simulation
from roundabout import rondo_run_sim

def sim_summary(cars_out_list, name=None, extended_summary=False):
    print("_"*80)
    print(f"\n---{name}---\n")
    for i in range(0, len(cars_out_list[0])):
        print(i+1, end=". ")
        if extended_summary:
            print(cars_out_list[0][i].arrival_time, end=" ")
            print(cars_out_list[0][i].entry_direction, end="--->")
            print(cars_out_list[0][i].destination_direction, end=" ")
            print(cars_out_list[0][i].segment_drive_time, end=" ")
        print(
            f"Czas przejazdu auta: {cars_out_list[1][i] - cars_out_list[0][i].arrival_time}")
    print(f"\nIle aut przejechało w symulacji: {len(cars_out_list[0])}\n")
    print("Sprawność {} wynosi: {}\n".format(
        "ronda" if name == "Roundabout" else "skrzyżowania", calculate_sim_time(cars_out_list)))
    # print("Ile aut razem (sym + w czsie rozgrzewania): {}".format(len(cars_list)))

def calculate_sim_time(cars_out_list):
    main_weight = 2
    side_weight = 1.5
    main_time_in_sim = 0
    side_time_in_sim = 0

    car_counter = len(cars_out_list[0])
    counter = 0
    for i in range(0, len(cars_out_list[0])):
        if "main" in cars_out_list[0][i].entry_direction:
            main_time_in_sim += cars_out_list[1][i] - \
                cars_out_list[0][i].arrival_time
            counter += 1
        elif "side" in cars_out_list[0][i].entry_direction:
            side_time_in_sim += cars_out_list[1][i] - \
                cars_out_list[0][i].arrival_time
            counter += 1
        else:
            raise Exception("Incorrect car entry_direction: {}".format(
                cars_out_list[0][i].entry_direction))
    output_time = ((main_weight * main_time_in_sim) ** 2 + (side_weight *
                    side_time_in_sim) ** 2) / (car_counter*main_weight*side_weight)**2 if car_counter != 0 else 1
    return output_time

def sim_call(summary, sim_time, warm_up_time, traffic_intensity, segment_drive_time_distribution,
                percentage_cars_on_main_road, force_intensity, starting_drive_time_distribution):

    sim = Simulation(sim_time, warm_up_time, traffic_intensity, segment_drive_time_distribution,
                        percentage_cars_on_main_road, force_intensity, starting_drive_time_distribution)

    sim.generate_cars_list()
    cars_list = sim.get_cars_list()

    events_list = []
    for car in cars_list:
        events_list.append(Event(car))

    cars_out_intersection = Intersection(events_list).run_sim(
        sim_time, warm_up_time, describe=False)
    cars_out_rnd = rondo_run_sim(
        sim.get_cars_list(), warm_up_time, sim_time)

    if summary:
        sim_summary(cars_out_intersection,
                    "Intersection", extended_summary=True)
        sim_summary(cars_out_rnd, "Roundabout", extended_summary=True)

    return cars_out_intersection, cars_out_rnd

def make_chart(int_times, rnd_times):
    plt.plot(int_times, 'g*', label="intersection")
    plt.plot(rnd_times, 'ro', label="roundabout")
    plt.legend()
    plt.xlabel("data sets")
    plt.ylabel("time")
    plt.grid()
    plt.show()