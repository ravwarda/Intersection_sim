class Event:
    def __init__(self, car, time=None, ev_type="in"):
        self.type = ev_type
        self.car = car
        if ev_type == "in":
            self.time = self.car.arrival_time
        elif ev_type == "out" or ev_type == "end":
            self.time = time
        else:
            raise Exception("Invalid event type")

