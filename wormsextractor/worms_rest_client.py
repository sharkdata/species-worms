#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2019-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import json
import urllib.request

from wormsextractor import worms_sqlite_cache


class WormsRestWebserviceClient:
    """ 
        For usage instructions check "https://github.com/sharkdata/species".
    """

    def __init__(self):
        """ """
        self.db_cache = worms_sqlite_cache.WormsSqliteCache()

    def get_aphia_id_by_name(self, scientific_name):
        """ WoRMS REST: AphiaIDByName. """
        # Check db cache.
        if self.db_cache.contains_name_to_id(scientific_name):
            aphia_id = self.db_cache.get_name_to_id(scientific_name)
            error = ""
            return (aphia_id, error)

        # Ask REST API.
        # url = 'http://www.marinespecies.org/rest/AphiaIDByName/' + scientific_name + '?marine_only=true'
        url = (
            "http://www.marinespecies.org/rest/AphiaIDByName/"
            + scientific_name
            + "?marine_only=false"
        )
        url = url.replace(" ", "%20")
        result = ""
        error = ""
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result = json.loads(response.read().decode("utf-8"))
                else:
                    error = (
                        "Species: "
                        + scientific_name
                        + "  Response code: "
                        + str(response.getcode())
                    )
        except Exception as e:
            error = "Species: " + scientific_name + "  Exception: " + str(e)

        # Save to db cache.
        self.db_cache.add_name_to_id(scientific_name, result)
        #
        return (result, error)

    def get_record_by_aphiaid(self, aphia_id):
        """  WoRMS REST: AphiaRecordByAphiaID """
        # Check db cache.
        if self.db_cache.contains_worms_record(aphia_id):
            worms_record = self.db_cache.get_worms_record(aphia_id)
            error = ""
            return (worms_record, error)

        # Ask REST API.
        url = "http://www.marinespecies.org/rest/AphiaRecordByAphiaID/" + str(aphia_id)
        result_dict = {}
        error = ""
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result_dict = json.loads(response.read().decode("utf-8"))
                else:
                    error = (
                        "AphiaID: "
                        + str(aphia_id)
                        + "  Response code: "
                        + str(response.getcode())
                    )
        except Exception as e:
            error = "AphiaID: " + str(aphia_id) + "  Exception: " + str(e)

        # Save to db cache.
        self.db_cache.add_worms_record(aphia_id, result_dict)
        #
        return (result_dict, error)

    def get_records_by_name(self, scientific_name):
        """  WoRMS REST: AphiaRecordsByName """
        # Check db cache.
        if self.db_cache.contains_records_by_name(scientific_name):
            worms_record = self.db_cache.get_records_by_name(scientific_name)
            error = ""
            return (worms_record, error)

        url = (
            "http://www.marinespecies.org/rest/AphiaRecordsByName/"
            + scientific_name
            + "?like=false&marine_only=false"
        )
        url = url.replace(" ", "%20")
        result_list = []
        error = ""
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result_list = json.loads(response.read().decode("utf-8"))
                else:
                    error = (
                        "Species: "
                        + scientific_name
                        + "  Response code: "
                        + str(response.getcode())
                    )
        except Exception as e:
            error = "Species: " + scientific_name + "  Exception: " + str(e)

        # Save to db cache.
        self.db_cache.add_records_by_name(scientific_name, result_list)
        #
        return (result_list, error)

    def get_classification_by_aphiaid(self, aphia_id):
        """  WoRMS REST: AphiaClassificationByAphiaID """
        # Check db cache.
        if self.db_cache.contains_classification(aphia_id):
            worms_record = self.db_cache.get_classification(aphia_id)
            error = ""
            return (worms_record, error)

        # Ask REST API.
        url = "http://www.marinespecies.org/rest/AphiaClassificationByAphiaID/" + str(
            aphia_id
        )
        result_dict = {}
        error = ""
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result_dict = json.loads(response.read().decode("utf-8"))
                else:
                    error = (
                        "AphiaID: "
                        + str(aphia_id)
                        + "  Response code: "
                        + str(response.getcode())
                    )
        except Exception as e:
            error = "AphiaID: " + str(aphia_id) + "  Exception: " + str(e)

        # Save to db cache.
        self.db_cache.add_classification(aphia_id, result_dict)
        #
        return (result_dict, error)
