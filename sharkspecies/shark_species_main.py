#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2019 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib

import worms_rest_client

class SharkSpeciesListGenerator():
    """ 
        For usage instructions check "https://github.com/sharkdata/species".
    """
    def __init__(self):
        """ """
        self.clear()
        # Create client for the REST API.
        self.worms_client = worms_rest_client.WormsRestWebserviceClient()
        #
        self.define_out_headers()

    def clear(self):
        """ """
        # Indata:
        self.indata_header = None
        self.indata_species_list = [] # Rank: Species or below.
        self.old_taxa_worms_dict = {} # Key: scientific_name.
        self.old_translate_worms_dict = {} # Key: scientific_name.
        # Outdata.
        self.taxa_worms_header = {}
        self.taxa_worms_dict = {} # Key: scientific_name.
        self.translate_to_worms_header = {}
        self.translate_to_worms_dict = {} # Key: scientific_name.
        # Errors.
        self.errors_list = []
        # Working area.
        self.higher_taxa_dict = {} # Key: aphia_id.
    
    def define_out_headers(self):
        """ """
        self.translate_to_worms_header = [
            'scientific_name_from', 
            'aphia_id_from', 
            'dyntaxa_from', 
            'scientific_name_to', 
            'aphia_id_to', 
            'dyntaxa_to',
            ]
        
        self.rename_worms_header_items = {
            'AphiaID': 'aphia_id', 
            'valid_AphiaID': 'valid_aphia_id', 
            'scientificname': 'scientific_name', 
            }
        
        self.taxa_worms_header = [
            'scientific_name',
            'rank',
            'aphia_id',
            'parent_name', 
            'parent_id', 
            'authority',
            'status',
            'kingdom',
            'phylum',
            'class',
            'order',
            'family',
            'genus',
            'classification', 
#             'isBrackish',
#             'isExtinct',
#             'isFreshwater',
#             'isMarine',
#             'isTerrestrial',
#             'unacceptreason',
#             'valid_AphiaID',
#             'valid_authority',
#             'valid_name',
#             'citation',
#             'url',
#             'lsid',
#             'match_type',
#             'modified',
            ]
    
    def run_all(self):
        """ """
        print('\nSpecies list generator started.')
        # Step 1. Import list containing scientific names. 
        #         Rank: Species and below to avoid homonym problems for higher taxa.
        self.import_species_list()
        
        # Step 2. Import old versions of "taxa" and "translate" if they are available.
        #         Put them in the "data_in" folder if you just want to add a few new 
        #         taxa to the lists. The translate list can be used for taxa that are 
        #         problematic to automatically find in WoRMS.
        self.import_old_taxa_worms()
        self.import_old_translate_to_worms()
        
        # Step 3. Iterate over taxa. Call WoRMS if not in old "taxa" or "translate".
        for species in sorted(self.indata_species_list):
            # Check if it's already translated. 
            aphia_id = ''
            if species in self.old_translate_worms_dict:
                scientific_name = self.old_translate_worms_dict[species].get('scientific_name_to', '')
                aphia_id = self.old_translate_worms_dict[species].get('aphia_id_to', '')
            else:
                scientific_name = species
            
            # Don't ask WoRMS if it is in the old list.
            if scientific_name not in self.old_taxa_worms_dict:
                
                print('- Processing: ', scientific_name)
                
                if not aphia_id:
                    aphia_id, error = self.worms_client.get_aphia_id_by_name(scientific_name)
                    if error:
                        self.errors_list.append([scientific_name, '', error])
                        aphia_id = ''
                        
                if aphia_id:
                    worms_rec, error = self.worms_client.get_record_by_aphiaid(aphia_id)
                    if error:
                        self.errors_list.append(['', aphia_id, error])
                    else:
                        # Replace 'None' by space.
                        for key in worms_rec.keys():
                            if worms_rec[key] in ['None', None]:
                                worms_rec[key] = ''
                        # Translate keys from WoRMS.
                        for from_key, to_key in self.rename_worms_header_items.items():
                            worms_rec[to_key] = worms_rec.get(from_key, '')
                        # 
                        aphia_id = worms_rec.get('AphiaID', '')
#                         name = worms_rec.get('scientificname', '')
                        valid_aphia_id = worms_rec.get('valid_AphiaID', '')
                        valid_name = worms_rec.get('valid_name', '')
                        
                        # Use valid taxa. 
                        if aphia_id == valid_aphia_id:
                            self.taxa_worms_dict[scientific_name] = worms_rec
                        else:
                            # aphia_id, error = worms_rest_client.get_aphia_id_by_name(valid_name)
                            if valid_name not in self.taxa_worms_dict:
                                worms_rec, error = self.worms_client.get_record_by_aphiaid(valid_aphia_id)
                                if error:
                                    self.errors_list.append(['', valid_aphia_id, error])
                                # Replace 'None' by space.
                                for key in worms_rec.keys():
                                    if worms_rec[key] in ['None', None]:
                                        worms_rec[key] = ''
                                # Translate keys from WoRMS.
                                for from_key, to_key in self.rename_worms_header_items.items():
                                    worms_rec[to_key] = worms_rec.get(from_key, '')
                                #
                                self.taxa_worms_dict[valid_name] = worms_rec
                            # Add invalid names to translate file.
                            if scientific_name not in self.translate_to_worms_dict:
                                translate_dict = {}
                                translate_dict['scientific_name_from'] = scientific_name
                                translate_dict['scientific_name_to'] = valid_name
                                translate_dict['aphia_id_from'] = aphia_id
                                translate_dict['aphia_id_to'] = valid_aphia_id
                                self.translate_to_worms_dict[scientific_name] = translate_dict
                        
                        # Step 5. Create classification dictionary.
                        worms_rec, error = self.worms_client.get_classification_by_aphiaid(valid_aphia_id)
                        if error:
                            self.errors_list.append(['', valid_aphia_id, error])
                        # Replace 'None' by space.
                        for key in worms_rec.keys():
                            if worms_rec[key] in ['None', None]:
                                worms_rec[key] = ''
                        # Translate keys from WoRMS.
                        for from_key, to_key in self.rename_worms_header_items.items():
                            worms_rec[to_key] = worms_rec.get(from_key, '')
                        #
                        aphia_id = None
                        rank = None
                        scientific_name = None
                        current_node = worms_rec
                        while current_node is not None:
                            parent_id = aphia_id
#                             parent_rank = rank
                            parent_name = scientific_name
                            aphia_id = current_node.get('AphiaID', '')
                            rank = current_node.get('rank', '')
                            scientific_name = current_node.get('scientificname', '')
                            if aphia_id and rank and scientific_name:
                                taxa_dict = {}
                                taxa_dict['aphia_id'] = aphia_id
                                taxa_dict['rank'] = rank
                                taxa_dict['scientific_name'] = scientific_name
                                taxa_dict['parent_id'] = parent_id
                                taxa_dict['parent_name'] = parent_name
                                # Replace 'None' by space.
                                for key in taxa_dict.keys():
                                    if taxa_dict[key] in ['None', None]:
                                        taxa_dict[key] = ''
                                if aphia_id not in self.higher_taxa_dict:
                                    self.higher_taxa_dict[aphia_id] = taxa_dict
                                current_node = current_node.get('child', None)
                            else:
                                current_node = None
                    
        # Step 4. Add higher taxa to WoRMS dictionary.
        for aphia_id, worms_dict in self.higher_taxa_dict.items():
            scientific_name = worms_dict.get('scientific_name', '')
            if scientific_name not in self.taxa_worms_dict:
                
                print('- Processing higher taxa: ', scientific_name)

                worms_rec, error = self.worms_client.get_record_by_aphiaid(aphia_id)
                if error:
                    self.errors_list.append(['', aphia_id, error])
                # Replace 'None' by space.
                for key in worms_rec.keys():
                    if worms_rec[key] in ['None', None]:
                        worms_rec[key] = ''
                # Translate keys from WoRMS.
                for from_key, to_key in self.rename_worms_header_items.items():
                    worms_rec[to_key] = worms_rec.get(from_key, '')
                    
                self.taxa_worms_dict[scientific_name] = worms_rec
        
        # Step 5. Add parent info to built classification hierarchies.
        for scientific_name, taxa_dict in self.taxa_worms_dict.items():
            aphia_id = taxa_dict.get('AphiaID', '')
            higher_taxa_dict = self.higher_taxa_dict.get(aphia_id, None)
            if higher_taxa_dict:
                taxa_dict['parent_id'] = higher_taxa_dict.get('parent_id', '')
                taxa_dict['parent_name'] = higher_taxa_dict.get('parent_name', '')
        
        # Step 6. Add old taxa.
        for scientific_name in self.old_taxa_worms_dict.keys():
            if scientific_name not in self.taxa_worms_dict:
                self.taxa_worms_dict[scientific_name] = self.old_taxa_worms_dict[scientific_name]

        # Step 7. Add old translate.
        for scientific_name in self.old_translate_worms_dict.keys():
            if scientific_name not in self.translate_to_worms_dict:
                self.translate_to_worms_dict[scientific_name] = self.old_translate_worms_dict[scientific_name]
        
        # Step 8. Add classification.
        for scientific_name in list(self.taxa_worms_dict.keys()):
            classification_list = []
            taxon_dict = self.taxa_worms_dict[scientific_name]
            while taxon_dict:
                classification_list.append('[' + taxon_dict.get('rank', '') + '] ' + taxon_dict.get('scientific_name', ''))
                # Parents.
                parent_name = taxon_dict.get('parent_name', '')
                taxon_dict = self.taxa_worms_dict.get(parent_name, None)
            #
            self.taxa_worms_dict[scientific_name]['classification'] = ' - '.join(classification_list[::-1])
        
        # Step 9. Save errors.
        self.save_errors()
        
        # Step 10. Save the results.
        self.save_taxa_worms()
        self.save_translate_to_worms()
        
        print('\nDone...')
    
    def import_species_list(self):
        """ """
        indata_species = pathlib.Path('data_in/indata_species_by_name.txt')
        if indata_species.exists():
            print('Importing file: ', indata_species)
            with indata_species.open('r', encoding='cp1252', errors = 'ignore') as indata_file:
                for row in indata_file:
                    row = row.strip()
                    if row:
                        if self.indata_header is None:
                            self.indata_header = row
                        else:
                            if (len(row) > 4) and (' ' in row):
                                self.indata_species_list.append(row)
                            else:
                                print('- Species not valid: ', row)
            print('')
        
    def import_old_taxa_worms(self):
        """ """
        indata_worms = pathlib.Path('data_in/taxa_worms.txt')
        if indata_worms.exists():
            print('Importing file: ', indata_worms)
            with indata_worms.open('r', encoding='cp1252', errors = 'ignore') as indata_file:
                header = None
                for row in indata_file:
                    row = [item.strip() for item in row.strip().split('\t')]
                    if header is None:
                        header = row
                    else:
                        row_dict = dict(zip(header, row))
                        scientific_name = row_dict.get('scientificname', '')
                        if scientific_name:
                            self.old_taxa_worms_dict[scientific_name] = row_dict
            print('')
    
    def import_old_translate_to_worms(self):
        """ """
        indata_translate = pathlib.Path('data_in/translate_to_worms.txt')
        if indata_translate.exists():
            print('Importing file: ', indata_translate)
            with indata_translate.open('r', encoding='cp1252', errors = 'ignore') as indata_file:
                header = None
                for row in indata_file:
                    row = [item.strip() for item in row.strip().split('\t')]
                    if header is None:
                        header = row
                    else:
                        row_dict = dict(zip(header, row))
                        scientific_name = row_dict.get('scientific_name_from', '')
                        if scientific_name:
                            self.old_translate_worms_dict[scientific_name] = row_dict
            print('')
    
    def save_taxa_worms(self):
        """ """
        taxa_worms_file = pathlib.Path('data_out/taxa_worms.txt')
        with taxa_worms_file.open('w', encoding='cp1252', errors = 'ignore') as outdata_file:
            outdata_file.write('\t'.join(self.taxa_worms_header) + '\n')
            for _taxa, taxa_rec in self.taxa_worms_dict.items():
                row = []
                for header_item in self.taxa_worms_header:
                    row.append(str(taxa_rec.get(header_item, '')))
                try:
                    outdata_file.write('\t'.join(row) + '\n')
                except Exception as e:
                    try: print('Exception when writing to taxa_worms.txt: ', row[0], '   ', e)
                    except: pass
                    
    def save_translate_to_worms(self):
        """ """
        taxa_worms_file = pathlib.Path('data_out/translate_to_worms.txt')
        with taxa_worms_file.open('w', encoding='cp1252', errors = 'ignore') as outdata_file:
            outdata_file.write('\t'.join(self.translate_to_worms_header) + '\n')
            for taxa_rec in self.translate_to_worms_dict.values():
                row = []
                for header_item in self.translate_to_worms_header:
                    row.append(str(taxa_rec.get(header_item, '')))
                try:
                    outdata_file.write('\t'.join(row) + '\n')
                except Exception as e:
                    try: print('Exception when writing to taxa_worms.txt: ', row[0], '   ', e)
                    except: pass
    
    def save_errors(self):
        """ """
        header = ['scientific_name', 'aphia_id', 'error']
        errors_file = pathlib.Path('data_out/errors.txt')
        with errors_file.open('w', encoding='cp1252', errors = 'ignore') as outdata_file:
            outdata_file.write('\t'.join(header) + '\n')
            for row in self.errors_list:
                try:
                    outdata_file.write('\t'.join(row) + '\n')
                except Exception as e:
                    try: print('Exception when writing to taxa_worms.txt: ', row[0], '   ', e)
                    except: pass


##### MAIN ########################################
if __name__ == "__main__":
    """ """
    taxa_mgr = SharkSpeciesListGenerator()
    
    taxa_mgr.run_all()

