
class Car:
    def __init__(self, arrival_time=0, time_to_force=0, entry_direction=None,
                 destination_direction=None, segment_drive_time=3, starting_drive_time=5, is_analyzed=True):
        self.arrival_time = arrival_time  # czas wjechania na skrzyżowanie
        # czas po jakim nastąpi wymuszenie pierwszeństwa
        self.time_to_force = time_to_force
        # kierunek z którego auto wjechało na skrzyżowanie
        self.entry_direction = entry_direction
        # kierunek do którego auto zmierza
        self.destination_direction = destination_direction
        # czy auto jest w ruchu czy stoi (czy doliczamy czas ruszania)
        self.is_moving = True
        # czas na przejechanie segmentu
        self.segment_drive_time = segment_drive_time
        # dodatkowy czas na ruszenie po zatrzymaniu
        self.starting_drive_time = starting_drive_time
        # flaga czy auto ma być badane czy nie
        self.is_analyzed = is_analyzed
        self.number = None  # numer jest mi potrzebny do wizualizacji działania symulacji

    def change_moving_state(self):
        self.is_moving = not self.is_moving
