from car import Car as Car


class Segment:
    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type
        self.occupied = False
        self.o_car = None
        self.state_change_time = None
        self.next_segment = None  # Dodane next_segment

    def occupy(self, car, time):
        self.occupied = True
        self.o_car = car
        self.state_change_time = time

    def release(self):
        self.occupied = False
        self.o_car = None
        self.state_change_time = None


def rondo_run_sim(cars, sim_time, start_time):
    # niech cars to lista posortowanych według czasu aut

    # Cztery kolejki aut (pierwszy zjazd, drugi, trzeci i czwarty)
    queues = [[], [], [], []]

    # Tworzenie ośmiu segmentów
    segment1 = Segment("main1", "out")
    segment2 = Segment("main1", "in")  # kolejka 1
    segment3 = Segment("side1", "out")
    segment4 = Segment("side1", "in")  # kolejka 2
    segment5 = Segment("main2", "out")
    segment6 = Segment("main2", "in")  # kolejka 3
    segment7 = Segment("side2", "out")
    segment8 = Segment("side2", "in")  # kolejka 4

    # Łączenie segmentów
    segments = [segment1, segment2, segment3, segment4,
                segment5, segment6, segment7, segment8]
    for i in range(8):
        segments[i].next_segment = segments[(i + 1) % 8]

    # for i in range(8):
    #     print(segments[i].name, end="--->")
    #     print(segments[i].next_segment.name, sep=" ")
    #     print(segments[i].next_segment.type)
    # lista aut, które wyjechały:
    cars_out = [[], []]

    def sim_time_search(sys_time):

        # Używam filter, aby uzyskać tylko odpowiednie segmenty
        filtered_segments = filter(lambda seg: seg.state_change_time is not None and seg.state_change_time > sys_time,
                                   segments)

        # Użyj min, aby znaleźć minimalną wartość z odpowiednich segmentów
        min_seg = min(
            (seg.state_change_time for seg in filtered_segments), default=99999999999)

        cars_time = []
        for queue in queues:
            if len(queue) > 0:
                if queue[0].time_to_force > sys_time:
                    cars_time.append(queue[0].time_to_force)

        if len(cars_time) > 0:
            min_time_to_force = min(car for car in cars_time)
        else:
            min_time_to_force = 999999999

        if len(cars) > 0:
            min_cars = cars[0].arrival_time
        else:
            min_cars = 999999999
    # zwraca nowy sys_time
        my_min = min(min_seg, min_time_to_force, min_cars, end_time)
        # print(my_min)
        return my_min

    def move_car(seg):
        seg.next_segment.occupy(
            car=seg.o_car, time=sys_time + seg.o_car.segment_drive_time)
        # jeśli ten, na które autko wjechało nie jest tym, z którego wyjedzie:
        if seg.next_segment.name != seg.o_car.destination_direction:
            seg.next_segment.next_segment.occupied = True  # od razu zaklepuje następny
        seg.release()  # zwalnia obecny segment
        state_change = True  # nastąpiła zmiana
        # print("Autko przesunęło się o segment")

    def handle_traffic_jam(sys_time):
        move_all = True
        for seg in segments:
            if seg.o_car is None:
                return False
            if seg.state_change_time > sys_time:
                move_all = False
        if move_all:
            next_seg = None
            moving_seg = segments[0]
            for seg in segments:
                next_seg = seg.next_segment
                move_car(moving_seg)
                moving_seg = next_seg

    def check_rondo_state(sys_time):
        state_change = True
        while state_change == True:
            state_change = False  # zmieniam flagę stanu

            for seg in segments:  # przeglądam wszystkie segmenty
                # sprawdzam, co mogę wykonać w tej chwili
                if seg.state_change_time is not None and seg.state_change_time <= sys_time:
                    if seg.o_car.destination_direction == seg.name:  # sprawdzam, czy autko jest już na ostanim segmencie
                        #    ----------wyjazd autka z ronda -----------------
                        if seg.o_car.is_analyzed:
                            cars_out[0].append(seg.o_car)  # dodaje autko
                            # dodaje czas, w którym wyjechał
                            cars_out[1].append(sys_time)
                        seg.release()  # usuwam autko z segmentu
                        state_change = True  # nastąpiła zmiana
                        # print("Autko wyjechało z ronda")
                        continue
                    else:  # jeśli autko nie jest na ostanim segmencie:
                        if seg.next_segment.o_car == None:  # jeśli nie ma autka na następnym wjeżdża na kolejny segment
                            seg.next_segment.occupy(
                                car=seg.o_car, time=sys_time + seg.o_car.segment_drive_time)

                            # jeśli ten, na które autko wjechało nie jest tym, z którego wyjedzie:
                            if seg.next_segment.name != seg.o_car.destination_direction:
                                seg.next_segment.next_segment.occupied = True  # od razu zaklepuje następny
                            seg.release()  # zwalnia obecny segment
                            state_change = True  # nastąpiła zmiana
                            # print("Autko przesunęło się o segment")

            handle_traffic_jam(sys_time)

    def queue_index(entry_dir):
        if entry_dir == "main1":
            return 0
        if entry_dir == "side1":
            return 1
        if entry_dir == "main2":
            return 2
        if entry_dir == "side2":
            return 3
        else:
            raise Exception("Invalid entry direction")

    def check_cars(sys_time):
        """Funkcja sprawdza auta z ogólnej listy aut, które jeszcze nie wjechały"""
        while len(cars) > 0 and sys_time == cars[0].arrival_time:
            ind = queue_index(cars[0].entry_direction)
            if len(queues[ind]) > 0:
                cars[0].is_moving = False
            else:
                # zmiana na czas bezwzględny czasu wymuszenia
                cars[0].time_to_force = cars[0].time_to_force + sys_time
            # if (sys_time>=start_time):
            #     cars[0].is_analyzed =  True
            # dodaje auto do odpowiedniej kolejki w zależności od kierunku wjazdu auta
            queues[ind].append(cars[0])
            cars.pop(0)  # usuwam autu z listy
            # print("Dodano auto do kolejki do skrzyżowania")

    def segment_index(no_queue):
        if no_queue == 0:
            return 1
        if no_queue == 1:
            return 3
        if no_queue == 2:
            return 5
        if no_queue == 3:
            return 7
        else:
            raise Exception("Invalid index of queue")

    def add_time_to_force(cars, sys_time):
        if len(cars) > 0:
            cars[0].time_to_force = sys_time + cars[0].time_to_force

    def force(sys_time):
        for i in range(0, 4):
            if len(queues[i]) == 0:
                continue
            if queues[i][0].time_to_force <= sys_time:  # próba wymuszenia
                if segments[segment_index(i)].o_car is None:
                    # segments[segment_index(i)].o_car = queues[i][0]
                    # segments[segment_index(i)].occupied = True
                    # segments[segment_index(i)].state_change_time = sys_time + segments[segment_index(i)].o_car.segment_drive_time
                    segments[segment_index(i)].occupy(
                        car=queues[i][0], time=sys_time + queues[i][0].segment_drive_time)
                    segments[segment_index(i)].next_segment.occupied = True
                    queues[i].pop(0)  # usuwam już autko z kolejki
                    # ---- tutaj następne autko musi zyskac czas na wymuszenie
                    add_time_to_force(cars=queues[i], sys_time=sys_time)
                    # print("Nastąpiło wymuszenie")
                    continue

    def moving_car_from_queue_to_rnd(i):
        added_time = 0
        if queues[i][0].is_moving:
            added_time = queues[i][0].starting_drive_time
            queues[i][0].is_moving = True
        segments[segment_index(i)].occupy(
            car=queues[i][0], time=sys_time + queues[i][0].segment_drive_time + added_time)
        segments[segment_index(i)].next_segment.occupied = True
        queues[i].pop(0)  # usuwam już autko z kolejki

    def check_entry_state(sys_time):
        # "Funkcja sprawdza czy jakieś autko może wjechać"
        for i in range(0, 4):
            if len(queues[i]) == 0:
                continue
            if queues[i][0].time_to_force <= sys_time:  # próba wymuszenia
                if segments[segment_index(i)].o_car is None:
                    moving_car_from_queue_to_rnd(i)
                    # ---- tutaj następne autko musi zyskac czas na wymuszenie
                    add_time_to_force(cars=queues[i], sys_time=sys_time)
                    # print("Autko wymusiło")
                    continue

            # wjechanie na rondo, wystarczy, że occupied is False
            if segments[segment_index(i)].occupied is False:
                moving_car_from_queue_to_rnd(i)
                add_time_to_force(cars=queues[i], sys_time=sys_time)
                # print("Autko wjechało na rondo")
                continue

    # def get_queue_index(self, entry_direction):
    #     # Funkcja do określenia indeksu kolejki na podstawie kierunku wjazdu i kierunku docelowego
    #     #"main1", "main2", "side1", "side2"
    #     if entry_direction == "main1":
    #         return 0
    #     elif entry_direction == "side1":
    #         return 1
    #     elif entry_direction == "main2" :
    #         return 2
    #     elif entry_direction == "side2":
    #         return 3
    #     else:
    #         # Obsługa innych przypadków, jeśli to konieczne
    #         return 0

    sys_time = 0
    end_time = start_time + sim_time

    while 1 > 0:
        sys_time = sim_time_search(sys_time)
        if sys_time >= end_time:
            # print("KONIEC SYMULACJI")
            break
        check_cars(sys_time)
        force(sys_time)
        check_rondo_state(sys_time)
        check_entry_state(sys_time)

    return cars_out
