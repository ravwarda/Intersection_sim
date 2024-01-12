import os
from generate_parameters import *
from simulation_functions import *


def execute_simulation():
    # ---Zmienne parametry  pomiędzy symulacjami:
    # natężenie ilości aut na całym skrzyżowaniu (czym mniejsza wartosc tym wiecej aut)
    traffic_intensity = 1
    # średnia dla rozkładu lognormalnego określająca czas przejechania przez segment skrzyżowania
    segment_drive_time_distribution = 1
    # ile procent aut przyjeżdża z jednego kierunku drogi głównej
    percentage_cars_on_main_road = 0.25

    # ---Stałe parametry początkowe dla wszystkich symulacji:
    # czas trwania symulacji [s]
    sim_time = 1000
    # czas na rozgrzanie symulacji - po jakim czasie działania symualcji [s] zaczynamy badanie
    warm_up_time = 600
    # średnia dla rozkładu lognormalnego określająca czas do wymuszenia [s]
    force_intensity = 3
    # średnia dla rozkładu lognormalnego określająca dodatkowy czas na rozpoczęcie jazdy po zatrzymaniu [s]
    starting_drive_time_distribution = 0.6

    force_intensity = force_intensity * segment_drive_time_distribution 
    starting_drive_time_distribution = starting_drive_time_distribution * segment_drive_time_distribution
    # czy wywołać pojedynczą sumulację dla danych powyżej czy dla wszystkich danych z pliku
    use_file = True
    generate_new_file = True

    if use_file:
        filename = "parameters.json"
        if (not os.path.isfile(filename) ) or generate_new_file:
            generate_parmeters_file(filename)
        parameters_list = get_parameters_from_file(filename)
        intersection_times = []
        roundabout_times = []
        for parmeters_dict in parameters_list:
            traffic_intensity = parmeters_dict['traffic']
            segment_drive_time_distribution = parmeters_dict['segment']
            percentage_cars_on_main_road = parmeters_dict['percentage']

            cars_out_intersection, cars_out_rnd = sim_call(False, sim_time, warm_up_time, traffic_intensity, segment_drive_time_distribution,
                                                           percentage_cars_on_main_road, force_intensity, starting_drive_time_distribution)
            intersection_times.append(
                calculate_sim_time(cars_out_intersection))
            roundabout_times.append(calculate_sim_time(cars_out_rnd))

        make_chart(intersection_times, roundabout_times)
    else:
        sim_call(True, sim_time, warm_up_time, traffic_intensity, segment_drive_time_distribution,
                 percentage_cars_on_main_road, force_intensity, starting_drive_time_distribution)


if __name__ == "__main__":
    execute_simulation()
