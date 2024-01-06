from event import Event


class Intersection:
    def __init__(self, events):
        self.sys_time = 0
        self.queues = [[], [], [], []]
        self.segments = []
        for i in range(0, 4):
            self.segments.append(self.Segment())
        self.events = events

    def run_sim(self, sim_time):
        self.events.append(Event(None, sim_time, "end"))
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
            for event in in_events:
                # dodawanie aut do kolejek
                pass
            for event in out_events:
                # zwalnianie sektorów
                pass
            # wpuszczanie aut na skrzyżowanie

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
