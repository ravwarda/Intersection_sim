The goal of this project was to develop two separate, but comparable, models that can simulate the flow of traffic both on a roundabout and a priority intersection. The simulation that is necessary to make a comparison between those two objects can be run in two different ways:

1. manually adjusting parameters of a single simulation
2. running multiple simulations based on parameters located in the 'parameters.json' file

Parameters that are possible to adjust are:

- traffic_intensity - average time between arrivals of vehicles
- segment_drive_time_distribution - average time that a vehicle needs to pass one part of an intersection
- percentage_cars_on_main_road - fraction of cars that arrive from one direction on main road (traffic coming from the opposite direction has the same intensity, and the remaining part is split between side roads)

The scenario is set to warm up for 10 minutes and then simulate another 60 minutes to gather results.
