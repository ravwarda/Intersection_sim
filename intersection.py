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

    # funkcja sprawdzająca, który samochód powinien wjechać na skrzyżowanie
    def check_priority(self, cars):
        def check_result():
            if len(result_cars) == 1:
                return result_cars[0]
            else:
                return min(result_cars, key=lambda x: x.time_to_force)

        if len(cars) == 1:
            return cars[0]
        result_cars = []
        # sprawdzanie wymuszeń
        for car in cars:
            if car.time_to_force <= self.sys_time:
                result_cars.append(car)
        if not result_cars:
            # sprawdzanie samochodów na drogach głównych
            for car in cars:
                if car_direction(car) in (0, 2):
                    result_cars.append(car)
        if not result_cars:
            # sprawdzanie samochodów na drogach podporządkowanych
            for car in cars:
                if car_direction(car) in (1, 3):
                    result_cars.append(car)
        return check_result()

    def calculate_out_event_time(self, car):
        entry = car_direction(car)
        destination = car_direction(car, destination=True)
        if entry > destination:
            destination += 4
        out_time = self.sys_time
        if destination - entry == 1:
            out_time += car.segment_drive_time * 1.5
        elif destination - entry == 2:
            out_time += car.segment_drive_time * 1
        elif destination - entry == 3:
            out_time += car.segment_drive_time * 1.7
        else:
            raise Exception("Car direction check error")
        if not car.is_moving:
            out_time += car.starting_drive_time
        return out_time

    def run_sim(self, sim_time, warm_up_time, describe=False):
        car_counter = 0
        result_cars = [[], []]
        self.events.append(Event(None, warm_up_time + sim_time, "end"))  # ustalenie momentu zakończenia symulacji

        # obsługa bieżących wydarzeń w symulacji
        while self.sys_time < warm_up_time + sim_time:
            self.sys_time = min(event.time for event in self.events)
            in_events = []
            out_events = []
            # ustalanie wydarzeń do obsłużenia
            for event in self.events:
                if event.time == self.sys_time:
                    if event.type == "in":
                        in_events.append(event)
                    elif event.type == "out":
                        out_events.append(event)
                    else:
                        return result_cars
                    self.events.remove(event)
            # dodawanie aut do kolejek
            for event in in_events:
                queue = self.queues[car_direction(event.car)]
                if queue:  # jeżeli kolejka nie jest pusta, zatrzymaj samochód
                    event.car.change_moving_state()
                queue.append(event.car)
                car_counter += 1
                event.car.number = car_counter
                if describe: print(f"{self.sys_time}: Samochód {event.car.number} dotarł do kolejki {event.car.entry_direction}, na {len(queue)} miejsce")
                event.car.time_to_force += self.sys_time
            # zwalnianie segmentów skrzyżowania
            for event in out_events:
                if describe: print(f"{self.sys_time}: Samochód {event.car.number} zjechał ze skrzyżowania, w drogę {event.car.destination_direction}")
                # if event.car.is_analyzed:
                if self.sys_time >= warm_up_time:
                    result_cars[0].append(event.car)
                    result_cars[1].append(event.time)
                for segment in self.segments:
                    if event.car == segment.o_car:
                        segment.release()
            # obsługa wpuszczania aut na skrzyżowanie
            while True:
                considered_cars = []
                for queue in self.queues:
                    if queue:
                        if self.segments_free(queue[0]):
                            considered_cars.append(queue[0])
                if not considered_cars:
                    break
                entering_car = self.check_priority(considered_cars)
                considered_cars.remove(entering_car)
                self.queues[car_direction(entering_car)].remove(entering_car)
                self.segments_free(entering_car, occupy=True)
                if describe: print(f"{self.sys_time}: Samochód {entering_car.number}, wjechał na skrzyżowanie, z kolejki {entering_car.entry_direction}, zmierza do {entering_car.destination_direction}")
                # if self.sys_time > warm_up_time:
                #     entering_car.is_analyzed = True
                event_time = self.calculate_out_event_time(entering_car)
                self.events.append(Event(entering_car, event_time, "out"))
            if considered_cars:
                for car in considered_cars:
                    car.is_moving = False

        return result_cars

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
