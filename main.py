from intersection import Intersection
from event import Event
from simulation import Simulation
from roundabout import rondo_run_sim

# funkcja generowania danych wejściowych
# funkcja do danych wyjściowych


def execute_simulation():
    def sim_summary(served_cars):
        print("________")

        for i in range(0, len(served_cars[0])):
            print(served_cars[0][i].arrival_time, end=" ")
            print(served_cars[0][i].entry_direction, end="--->")
            print(served_cars[0][i].destination_direction, end=" ")
            print(served_cars[0][i].segment_drive_time, end=" ")
            print(
                f"Całkowity czas przejazdu: {served_cars[1][i] - served_cars[0][i].arrival_time}")
        print("Ile aut w symulacji: {}".format(len(served_cars[0])))
        # print("Ile aut razem: {}".format(len(cars_list)))

    # ---Parametry początkowe:
    # czas trwania symulacji
    sim_time = 600
    # czas na rozgrzanie symulacji - po jakim czasie działania symualcji zaczynamy badanie
    warm_up_time = 200
    # natężenie ilości aut na całym skrzyżowaniu (czym mniejsza wartosc tym wiecej aut)
    traffic_intensity = 10
    # średnia dla rozkładu lognormalnego określająca czas przejechania przez segment skrzyżowania
    segment_drive_time_distribution = 1.5
    # ile procent aut przyjeżdża z jednego kierunku drogi głównej
    percentage_cars_on_main_road = 0.3
    # średnia dla rozkładu lognormalnego określająca czas do wymuszenia
    force_intensity = 4.5
    # średnia dla rozkładu lognormalnego określająca czas na rozpoczęcie jazdy po zatrzymaniu
    starting_drive_time_distribution = 2

    sim = Simulation(sim_time, warm_up_time, traffic_intensity, segment_drive_time_distribution,
                     percentage_cars_on_main_road, force_intensity, starting_drive_time_distribution)

    # sim = Simulation()

    sim.generate_cars_list()

    cars_list = sim.get_cars_list()

    events_list = []
    for car in cars_list:
        events_list.append(Event(car))
        # print(car.arrival_time)
    cars_out = Intersection(events_list).run_sim(sim_time, warm_up_time, describe=False)
    sim_summary(cars_out)

    cars, start_time, sim_time = sim.get_cars_list(), warm_up_time, sim_time

    # print(start_time, sim_time)
    # print(len(cars))
    cars_out = rondo_run_sim(cars, start_time, sim_time)
    sim_summary(cars_out)


if __name__ == "__main__":
    execute_simulation()
