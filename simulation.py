import numpy as np
import random
import copy
from car import Car


class Simulation:
    def __init__(self, sim_time=600, warm_up_time=200, traffic_intensity=5, segment_drive_time=3,
                 percentage_cars_on_main_road=0.3, force_intensity=20, starting_drive_time=5):
        self.sim_time = sim_time
        if sim_time < 0:
            raise Exception("sim_time value can't be negative")

        self.warm_up_time = warm_up_time
        if warm_up_time < 0:
            raise Exception("warm_up_time value can't be negative")

        self.traffic_intensity = traffic_intensity
        if traffic_intensity < 0:
            raise Exception("traffic_intensity value can't be negative")

        self.segment_drive_time = segment_drive_time
        if segment_drive_time < 0:
            raise Exception("segment_drive_time value can't be negative")

        self.percentage_cars_on_main_road = percentage_cars_on_main_road
        if percentage_cars_on_main_road < 0.25:
            raise Exception(
                "Main road has to have greater car intensity than side road")
        if percentage_cars_on_main_road > 0.5:
            raise Exception(
                "Too high percentage of cars on the main road (pr > 1)")

        self.force_intensity = force_intensity
        if force_intensity < 0:
            raise Exception("force_intensity value can't be negative")

        self.starting_drive_time = starting_drive_time
        if starting_drive_time < 0:
            raise Exception("starting_drive_time value can't be negative")
        
        self.cars_list = None

    def choose_direction(self, pass_direction=None):
        available_directions = ["main1", "main2", "side1", "side2"]

        pc_main = self.percentage_cars_on_main_road
        pc_side = (1 - self.percentage_cars_on_main_road * 2) / 2

        if pass_direction is None:
            # losujemy drogę początkową
            number = random.uniform(0, 1)
            if number < pc_main:
                dir_choice = available_directions[0]
            elif number < pc_main * 2:
                dir_choice = available_directions[1]
            elif number < pc_main * 2 + pc_side:
                dir_choice = available_directions[2]
            else:
                dir_choice = available_directions[3]
        elif "main" in pass_direction:
            # losujemy drogę docelową dla auta jadącego z drogi głownej
            number = random.uniform(0, 1 - pc_main)
            if number < pc_main:
                dir_choice = available_directions[0]
                if dir_choice == pass_direction:
                    dir_choice = available_directions[1]
            elif number < pc_main + pc_side:
                dir_choice = available_directions[2]
            else:
                dir_choice = available_directions[3]
        elif "side" in pass_direction:
            # losujemy drogę docelową dla auta jadącego z drogi podporządkowanej
            number = random.uniform(0, 1 - pc_side)
            if number < pc_main:
                dir_choice = available_directions[0]
            elif number < pc_main * 2:
                dir_choice = available_directions[1]
            else:
                dir_choice = available_directions[2]
                if dir_choice == pass_direction:
                    dir_choice = available_directions[3]
        else:
            raise Exception("Wrong direction name")

        return dir_choice

    def generate_cars_list(self):
        cars_list = []
        all_cars_time = 0

        while True:
            time_to_next_car = np.round(np.random.exponential(
                scale=self.traffic_intensity))

            all_cars_time += time_to_next_car

            time_to_force = np.round(np.random.exponential(
                scale=self.force_intensity, size=1))

            entry_direction = self.choose_direction()

            destination_direction = self.choose_direction(entry_direction)

            cars_list.append(Car(all_cars_time, time_to_force,
                             entry_direction, destination_direction))

            if all_cars_time > self.sim_time + self.warm_up_time:
                break

        self.cars_list = cars_list

    def get_cars_list(self):
        if self.cars_list is None:
            raise Exception("Can't get cars_list if it is empty")

        return copy.deepcopy(self.cars_list)