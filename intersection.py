from event import Event


class Intersection:
    def __init__(self, events):
        self.sys_time = 0
        self.queues = [[], [], [], []]
        self.segments = []
        for i in range(0, 4):
            self.segments.append(self.Segment())
        self.events = events

    # def check_priority(self, cars):


    def run_sim(self, sim_time):
        self.events.append(Event(None, sim_time, "end"))  # ustalenie momentu zakończenia symulacji

        # obsługa bieżących wydarzeń w symulacji
        while self.sys_time < sim_time:
            self.sys_time = min(event.time for event in self.events)
            in_events = []
            out_events = []
            for event in self.events:
                if event.time == self.sys_time:
                    if event.type == "in":
                        in_events.append(event)
                    else:
                        out_events.append(event)
                    self.events.remove(event)
            for event in in_events:  # dodawanie aut do kolejek
                if event.car.entry_direction == "main1":
                    self.queues[0].append(event.car)
                elif event.car.entry_direction == "side1":
                    self.queues[1].append(event.car)
                elif event.car.entry_direction == "main2":
                    self.queues[2].append(event.car)
                elif event.car.entry_direction == "side2":
                    self.queues[3].append(event.car)
            for event in out_events:  # zwalnianie segmentów skrzyżowania
                for segment in self.segments:
                    if event.car == segment.o_car:
                        segment.release()

            # obsługa wpuszczania aut na skrzyżowanie
            # considered_cars = []
            # for queue in self.queues:
            #     if queue:


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
