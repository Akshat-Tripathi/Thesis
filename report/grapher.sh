#!/bin/sh

python box_plotter.py --i experiments//results//mu_bound -v onramp -n mu_bound_all_loops --x_axis "N Onramp Segments"
python box_plotter.py --i experiments//results//mu_bound -v onramp -n mu_bound_last_3_loops --x_axis "N Onramp Segments" --skip 34
python box_plotter.py --i experiments//results//mu_bound -v onramp -n mu_bound_last_3_loops_after_onramp --x_axis "N Onramp Segments" --skip 50

python box_plotter.py --i experiments//results//sybils -v sybils -n sybils_all_loops --x_axis "N Sybils" --skip 1
python box_plotter.py --i experiments//results//sybils -v sybils -n sybils_last_3_loops --x_axis "N Sybils" --skip 34

python box_plotter.py --i experiments//results//history_size -v window_size -n history_size_all_loops --x_axis "History Size" --skip 1
python box_plotter.py --i experiments//results//history_size -v window_size -n history_size_last_3_loops --x_axis "History Size" --skip 34

python box_plotter.py --i experiments//results//n_bots_defence -v n -n n_bots_all_loops --x_axis "N Robots" --skip 1
python box_plotter.py --i experiments//results//n_bots_defence -v n -n n_bots_last_3_loops --x_axis "N Robots" --skip 34

python box_plotter.py --i experiments//results//contagion -v hops -n contagion_all_loops --x_axis "N Hops from Victim" --skip 1
python box_plotter.py --i experiments//results//contagion -v hops -n contagion_last_3_loops --x_axis "N Hops from Victim" --skip 34

python heatmapper.py --i experiments//results//startup_delay -v history_size delay -n startup_delay

python vs_time.py