
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

    # czy wywołać pojedynczą sumulację dla danych powyżej czy dla wszystkich danych z pliku
    use_file = True

    # ------------------------------

    force_intensity = force_intensity * segment_drive_time_distribution
    starting_drive_time_distribution = starting_drive_time_distribution * \
        segment_drive_time_distribution

    parameters = [sim_time, warm_up_time, traffic_intensity, segment_drive_time_distribution,
                  percentage_cars_on_main_road, force_intensity, starting_drive_time_distribution]

    if use_file:
        simulations_from_file(parameters, generate_new_file=True)
    else:
        sim_call(parameters, summary=False)


if __name__ == "__main__":
    execute_simulation()
