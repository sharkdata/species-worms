#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2019 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# import json
# import urllib.request
# import pandas as pd

class SharkSpecies():
    """ """
    def __init__(self):
        """ """
        # Indata.
        self.original_species_list = {} # Column: scientific_name.
        
        # AphiaID for original data.
        self.original_species_to_aphia_dict = {} # Key: scientific_name.
        self.missing_species_from_original_dict = {} # Key: scientific_name.

        # Valid and translate.
        self.valid_species_dict = {} # Key: scientific_name.
        self.translate_dict = {} # Key: scientific_name.
        
        # Classification.
        self.classification_dict = {} # Key: aphia_id.
        
        # Taxa info and taxa tree.
        self.taxa_info_dict = {} # Key: aphia_id.
        self.taxa_tree_dict = {} # Key: aphia_id.
        
    
    
    # Read the file from last year.
    peg_df = pd.read_excel('PEG_BVOL2018.xls', 
                               sep='\t', encoding='cp1252', na_filter=False,
                               usecols=['Species', 'AphiaID']
                               )
    print('Dataframe length: ', len(peg_df))
    peg_df
        
    
    unique_df = peg_df.drop_duplicates()
    print('Dataframe length: ', len(unique_df))
    unique_df.head()
    
    worms_df = pd.DataFrame()
    worms_df['Species'] = unique_df.Species
    worms_df['AphiaID'] = unique_df.AphiaID
    
    worms_df['worms_scientific_name'] = ''
    worms_df['worms_rank'] = ''
    worms_df['worms_status'] = ''
    worms_df['worms_valid_aphia_id'] = ''
    worms_df['worms_valid_name'] = ''
    worms_df['worms_rec_error'] = ''
    worms_df.head()
    
    # Apply.
    results = []
    results.append(worms_df.apply(apply_record_by_id, axis=1))
    
    worms_df['worms_scientific_name'] = [x[0] for x in results[0]]
    worms_df['worms_rank'] = [x[1] for x in results[0]]
    worms_df['worms_status'] = [x[2] for x in results[0]]
    worms_df['worms_valid_aphia_id'] = [x[3] for x in results[0]]
    worms_df['worms_valid_name'] = [x[4] for x in results[0]]
    worms_df['worms_rec_error'] = [x[5] for x in results[0]]
    
    
    worms_df.to_csv('HELCOM_PEG_2019_WoRMS_unique_taxa.txt', 
                     sep='\t', encoding='cp1252', index=False)
    
    species_df = pd.read_csv('HELCOM_PEG_2019_WoRMS_unique_taxa.txt', 
                             sep='\t', encoding='cp1252')
    species_df.fillna('', inplace=True)
    species_df.head()
    
    merged_df = pd.merge(peg_df, species_df,
                         how='left', on=['Species', 'AphiaID'])
    
    merged_df.to_csv('HELCOM_PEG_2019_WoRMS.txt', 
                     sep='\t', encoding='cp1252', index=False)
    
    species_df = pd.read_csv('HELCOM_PEG_2019_WoRMS_unique_taxa.txt', 
                             sep='\t', encoding='cp1252')
    species_df.fillna('', inplace=True)
    species_df.head()
    
    missing_df = species_df[species_df.AphiaID=='']
    
    scientific_name_array = missing_df.Species
    aphiaid_array, error_array = execute_id_by_name(scientific_name_array)
    
    result_df = pd.DataFrame()
    result_df['Species'] = scientific_name_array
    result_df['AphiaID'] = aphiaid_array
    result_df['worms_id_error'] = error_array
    result_df
       
    result_df.to_csv('HELCOM_PEG_2019_WoRMS_ID_search.txt', 
                     sep='\t', encoding='cp1252', index=False)
