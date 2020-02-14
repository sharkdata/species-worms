#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2019-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import json
import urllib.request


class WormsRestWebserviceClient:
    """ 
        For usage instructions check "https://github.com/sharkdata/species".
    """

    def __init__(self):
        """ """

    def get_aphia_id_by_name(self, scientific_name):
        """ WoRMS REST: AphiaIDByName. """
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
        #
        return (result, error)

    def get_record_by_aphiaid(self, aphia_id):
        """  WoRMS REST: AphiaRecordByAphiaID """
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
        #
        return (result_dict, error)

    def get_records_by_name(self, scientific_name):
        """  WoRMS REST: AphiaRecordsByName """
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
        #
        return (result_list, error)

    def get_classification_by_aphiaid(self, aphia_id):
        """  WoRMS REST: AphiaClassificationByAphiaID """
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
        #
        return (result_dict, error)
