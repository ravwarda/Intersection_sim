class Intersection:
    def __init__(self):
        self.sys_time = 0.0
        self.queues = [[], [], [], []]
        self.segments = []
        for i in range(0, 4):
            self.segments.append(self.Segment())

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
