#!/bin/bash

./mcnp6 tasks 4 n=facility0_wwn.txt                          && sleep 2
./mcnp6 tasks 4 n=facility1_wwn.txt                          && sleep 2
./mcnp6 tasks 4 n=facility2_wwn.txt wwinp=facility1_wwn.txte && sleep 2
./mcnp6 tasks 4 n=facility3_wwn.txt wwinp=facility2_wwn.txte && sleep 2
./mcnp6 tasks 4 n=facility4_wwn.txt wwinp=facility3_wwn.txte && sleep 2
./mcnp6 tasks 4 n=facility5_wwn.txt wwinp=facility4_wwn.txte && sleep 2

