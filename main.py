from simulation_functions import *
from tkinter import *
from tkinter.ttk import *


def execute_simulation(use_file=False, traffic_intensity = 2, segment_drive_time_distribution = 1, percentage_cars_on_main_road = 0.3):
    # ---Zmienne parametry pomiędzy symulacjami:
    # traffic_intensity - natężenie ilości aut na całym skrzyżowaniu (czym mniejsza wartosc tym wiecej aut)
    # segment_drive_time_distribution - średnia dla rozkładu lognormalnego określająca czas przejechania przez segment skrzyżowania
    # percentage_cars_on_main_road - ile procent aut przyjeżdża z jednego kierunku drogi głównej

    if percentage_cars_on_main_road <= 0 or percentage_cars_on_main_road > 0.5:
        print("Niewłaściwa wartość parametru ilości samochodów na grodze głównej")
        return 0

    # ---Stałe parametry początkowe dla wszystkich symulacji:
    # czas trwania symulacji [s]
    sim_time = 3600
    # czas na rozgrzanie symulacji - po jakim czasie działania symualcji [s] zaczynamy badanie
    warm_up_time = 600
    # średnia dla rozkładu lognormalnego określająca czas do wymuszenia [s]
    force_intensity = 4.5
    # średnia dla rozkładu lognormalnego określająca dodatkowy czas na rozpoczęcie jazdy po zatrzymaniu [s]
    starting_drive_time_distribution = 0.8
    starting_drive_time_distribution = (
            starting_drive_time_distribution * segment_drive_time_distribution
    )

    # ------------------------------

    parameters = [
        sim_time,
        warm_up_time,
        traffic_intensity,
        segment_drive_time_distribution,
        percentage_cars_on_main_road,
        force_intensity,
        starting_drive_time_distribution,
    ]

    if use_file:
        simulations_from_file(parameters, generate_new_file=True)
    else:
        cars_out_intersection, cars_out_rnd = Simulation(*parameters).sim_call()
        sim_summary(cars_out_intersection)
        sim_summary(cars_out_rnd)


def menu():
    root = Tk()

    lbl_sim = Label(root, text="Ustaw wartości parametrów dla symulacji, lub użyj wartości z pliku 'parameters.json'")

    lbl_ti = Label(root, text="Średni czas pomiędzy przyjazdami samochodów:")
    ti_var = IntVar()
    ti_var.set(2)
    ent_ti = Entry(root, textvariable=ti_var)

    lbl_sd = Label(root, text="Średni czas przejechania przez segment:")
    sd_var = IntVar()
    sd_var.set(1)
    ent_sd = Entry(root, textvariable=sd_var)

    lbl_pc = Label(root, text="Ułamek samochodów na drodze główniej (wartość: (0;0.5])")
    pc_var = DoubleVar()
    pc_var.set(0.3)
    ent_pc = Entry(root, textvariable=pc_var)

    btn_ssim = Button(root, text="Przeprowadź symulację", command=lambda: execute_simulation(False, ti_var.get(), sd_var.get(), pc_var.get()))

    btn_fsim = Button(root, text="Wyświetl analizę symulacji z parametrami z pliku", command=lambda: execute_simulation(True))

    lbl_sim.grid(row=0, column=0, pady=5)

    lbl_ti.grid(row=1, column=0, pady=3)
    ent_ti.grid(row=2, column=0, pady=3)
    lbl_sd.grid(row=3, column=0, pady=3)
    ent_sd.grid(row=4, column=0, pady=3)
    lbl_pc.grid(row=5, column=0, pady=3)
    ent_pc.grid(row=6, column=0, pady=3)

    btn_ssim.grid(row=7, column=0, pady=5)
    btn_fsim.grid(row=8, column=0, pady=10)

    root.mainloop()


if __name__ == "__main__":
    # execute_simulation()
    menu()
