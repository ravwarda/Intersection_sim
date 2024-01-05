
class Car:
    def __init__(self, arrival_time=0, time_to_force=0, entry_direction=None, destination_direction=None):
        self.arrival_time = arrival_time  # czas wjechania na skrzyżowanie
        # czas po jakim nastąpi wymuszenie pierwszeństwa
        self.time_to_force = time_to_force
        # kierunek z którego auto wjechało na skrzyżowanie
        self.entry_direction = entry_direction
        # kierunek do którego auto zmierza
        self.destination_direction = destination_direction
        # czy auto jest w ruchu czy stoi (doliczamy czas ruszania)
        self.is_moving = False

    def change_moving_state(self):
        self.is_moving = not self.is_moving


