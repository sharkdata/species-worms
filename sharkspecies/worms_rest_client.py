#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2019 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import json
import urllib.request

class WormsRestWebserviceClient():
    """ """
    def __init__(self):
        """ """
    
    def get_aphia_id_by_name(self, scientific_name):
        """ WoRMS REST: AphiaIDByName. """
        url = 'http://www.marinespecies.org/rest/AphiaIDByName/' + scientific_name + '?marine_only=true'
        url = url.replace(' ', '%20')
        result = ''
        error = ''
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result = json.loads(response.read().decode('utf-8'))
                else:
                    error = 'Species: ' + scientific_name + '  Response code: ' + str(response.getcode())
        except Exception as e:
            error = 'Species: ' + scientific_name + '  Exception: ' + str(e)
        #
        return (result, error)
     
    def get_record_by_aphiaid(self, aphia_id):
        """  WoRMS REST: AphiaRecordByAphiaID """
        url = 'http://www.marinespecies.org/rest/AphiaRecordByAphiaID/' + str(aphia_id)
        #print(url)
        #url = url.replace(' ', '%20')
        result_dict = {}
        error = ''
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result_dict = json.loads(response.read().decode('utf-8'))
                else:
                    error = 'AphiaID: ' + str(aphia_id) + '  Response code: ' + str(response.getcode())
        except Exception as e:
            error = 'AphiaID: ' + str(aphia_id) + '  Exception: ' + str(e)
        #
        return (result_dict, error)
     
    def get_classification_by_aphiaid(self, aphia_id):
        """  WoRMS REST: AphiaClassificationByAphiaID """
        url = 'http://www.marinespecies.org/rest/AphiaClassificationByAphiaID/' + str(aphia_id)
        #print(url)
        #url = url.replace(' ', '%20')
        result_dict = {}
        error = ''
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result_dict = json.loads(response.read().decode('utf-8'))
                else:
                    error = 'AphiaID: ' + str(aphia_id) + '  Response code: ' + str(response.getcode())
        except Exception as e:
            error = 'AphiaID: ' + str(aphia_id) + '  Exception: ' + str(e)
        #
        return (result_dict, error)
     
#     def apply_record_by_id(self, df_row):
#         """ """
#         worms_scientific_name = df_row.worms_scientific_name
#         worms_rank = df_row.worms_rank 
#         worms_status = df_row.worms_status
#         worms_valid_aphia_id = df_row.worms_valid_aphia_id 
#         worms_valid_name = df_row.worms_valid_name 
#         worms_rec_error = '' 
#         if df_row.AphiaID:
#             if df_row.worms_scientific_name == '':
#                 record_dict, error = self.get_record_by_aphiaid(df_row.AphiaID)
#                 worms_scientific_name = record_dict.get('scientificname', '')
#                 worms_rank = record_dict.get('rank', '')
#                 worms_status = record_dict.get('status', '')
#                 worms_valid_aphia_id = record_dict.get('valid_AphiaID', '')
#                 try:
#                     worms_valid_aphia_id = str(int(worms_valid_aphia_id)) # Remove decimal.
#                 except: pass
#                 worms_valid_name = record_dict.get('valid_name', '')
#                 worms_rec_error = error
#                 if error:
#                     print(error)
#         #
#         return [worms_scientific_name, worms_rank, worms_status, worms_valid_aphia_id, worms_valid_name, worms_rec_error]
#      
#      
#      
#     # Execute for all in array.
#     def execute_id_by_name(self, scientific_name_array):
#         aphiaid_array = []
#         error_array = []
#         for scientific_name in scientific_name_array:
#         #for scientific_name in taxa_df.scientific_name:
#             if ' ' in scientific_name:
#                 # Rank species or below.
#                 result, error = self.get_aphia_id_by_name(scientific_name)
#                 aphiaid_array.append(result)
#                 error_array.append(error)
#                 if error:
#                     print(error)
#             else:
#                 aphiaid_array.append('')
#                 error_array.append('(Higher rank)')
#         #
#         return (aphiaid_array, error_array)
     
