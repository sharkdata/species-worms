#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2019-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from . import wormsextractor

if __name__ == "__main__":
    """ """
    taxa_mgr = wormsextractor.SharkSpeciesListGenerator()
    
    taxa_mgr.run_all()
