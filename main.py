#!/usr/bin/python
# -*- coding: utf-8  -*-


# Dependancy for other element
import yaml
import sys
from pole_emploi import PoleEmplois


if __name__ == '__main__':
    # Read YML file
    with open("config.yml", 'r') as stream:
        data_loaded = yaml.load(stream)

    navigateur = PoleEmplois(data_loaded[sys.argv[2]][0],
                             data_loaded[sys.argv[2]][1])
