from intersection import Intersection
from event import Event
from simulation import Simulation


def execute_simulation():
    # ---Parametry początkowe:
    # czas trwania symulacji
    sim_time = 600
    # czas na rozgrzanie symulacji - po jakim czasie działania symualcji zaczynamy badanie
    warm_up_time = 200
    # natężenie ilości aut na całym skrzyżowaniu (czym mniejsza wartosc tym wiecej aut)
    traffic_intensity = 5
    # czas przejechania przez segment skrzyżowania
    segment_drive_time = 3
    # ile procent aut przyjeżdża z jednego kierunku drogi głównej
    percentage_cars_on_main_road = 0.3
    # natężenie częstości wymuszania pierwszeństwa
    force_intensity = 20
    # dodatkowy czas na rozpoczęcie jazdy po zatrzymaniu
    starting_drive_time = 5

    sim = Simulation(sim_time, warm_up_time, traffic_intensity, segment_drive_time,
                     percentage_cars_on_main_road, force_intensity, starting_drive_time)

    # sim = Simulation()

    sim.generate_cars_list()

    cars_list = sim.get_cars_list()  # tak sobie pobierajcie listę aut
    events_list = []
    for car in cars_list:
        events_list.append(Event(car))
    Intersection(events_list).run_sim(sim_time)


if __name__ == "__main__":
    execute_simulation()

