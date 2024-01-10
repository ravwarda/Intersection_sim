from event import Event


# funkcja zwracająca indeks kolejki, do której należy auto
def car_direction(car, destination=False):
    if destination:
        route = car.destination_direction
    else:
        route = car.entry_direction
    if route == "main1":
        return 0
    elif route == "side1":
        return 1
    elif route == "main2":
        return 2
    elif route == "side2":
        return 3
    else:
        return None


class Intersection:
    def __init__(self, events):
        self.sys_time = 0
        self.queues = [[], [], [], []]
        self.segments = []
        for i in range(0, 4):
            self.segments.append(self.Segment())
        self.events = events

    # funkcja sprawdzająca, czy segmenty, przez które musi przejechać samochód są wolne
    def segments_free(self, car, occupy=False):
        entry = car_direction(car)
        destination = car_direction(car, destination=True)
        while entry != destination:
            if self.segments[entry].occupied:
                return False
            if occupy:
                self.segments[entry].occupy(car)
            if entry == 3:
                entry = 0
            else:
                entry += 1
        return True

    # funkcja sprawdzająca,
    def check_priority(self, cars):
        def check_result():
            if len(result_cars) == 1:
                return result_cars
            else:
                return min(cars, key=lambda x: x.time_to_force)

        result_cars = []
        # sprawdzanie wymuszeń
        for car in cars:
            if car.time_to_force <= self.sys_time:
                result_cars.append(car)
        if result_cars:
            return check_result()
        # sprawdzanie pozostałych samochodów
        for car in cars:
            if car_direction(car) in (0, 2):
                result_cars.append(car)
        if result_cars:
            return check_result()
        for car in cars:
            if car_direction(car) in (1, 3):
                result_cars.append(car)
        return check_result()

    def run_sim(self, sim_time):
        self.events.append(Event(None, sim_time, "end"))  # ustalenie momentu zakończenia symulacji

        # obsługa bieżących wydarzeń w symulacji
        while self.sys_time < sim_time:
            self.sys_time = min(event.time for event in self.events)
            in_events = []
            out_events = []
            # ustalanie wydarzeń do obsłużenia
            for event in self.events:
                if event.time == self.sys_time:
                    if event.type == "in":
                        in_events.append(event)
                    else:
                        out_events.append(event)
                    self.events.remove(event)
            # dodawanie aut do kolejek
            for event in in_events:
                queue = self.queues[car_direction(event.car)]
                if queue: # jeżeli kolejka nie jest pusta, zatrzymaj samochód
                    event.car.change_moving_state()
                queue.append(event.car)
                event.car.time_to_force += self.sys_time
            # zwalnianie segmentów skrzyżowania
            for event in out_events:
                for segment in self.segments:
                    if event.car == segment.o_car:
                        segment.release()
            # obsługa wpuszczania aut na skrzyżowanie
            while True:
                considered_cars = []
                for queue in self.queues:
                    if queue:
                        if self.segments_free(queue[0]):
                            considered_cars.append(queue)
                if not considered_cars:
                    break
                self.segments_free(self.check_priority(considered_cars))

        return 0

    class Segment:
        def __init__(self):
            self.occupied = False
            self.o_car = None

        def occupy(self, car):
            self.occupied = True
            self.o_car = car

        def release(self):
            self.occupied = False
            self.o_car = None
