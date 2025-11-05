#!/bin/bash

python generate_base_model.py
python add_tallies.py
python cutout_shield.py
python remove_thermal_shield_base.py
python split_model.py
