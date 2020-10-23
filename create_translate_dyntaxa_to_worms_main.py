#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2019-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib

class CreateTranslateDyntaxaToWorms():
    """ """

    def __init__(self, data_in_path="data_in", data_out_path="data_out"):
        """ """
        self.data_in_path = data_in_path
        self.data_out_path = data_out_path
        #
        self.define_out_headers()
        #
        self.taxa_worms_dict = {}
        self.translate_to_worms_dict = {}

    def define_out_headers(self):
        """ """
        self.rename_worms_header_items = {
            "worms_scientific_name": "scientific_name",
            "worms_status": "status",
            "worms_valid_aphia_id": "",
            "worms_valid_name": "",
            "worms_rank": "rank",
            "worms_kingdom": "kingdom",
            "worms_phylum": "phylum",
            "worms_class": "v",
            "worms_order": "order",
            "worms_family": "family",
            "worms_genus": "genus",
            # "worms_rec_error": "",
            # "worms_lsid": "",
          }

        self.translate_dyntaxa_to_worms_header = [
            "scientific_name",
            "dyntaxa_id",
            "aphia_id",
            "worms_scientific_name",
            "worms_status",
            # "worms_valid_aphia_id",
            # "worms_valid_name",
            "worms_rank",
            "worms_kingdom",
            "worms_phylum",
            "worms_class",
            "worms_order",
            "worms_family",
            "worms_genus",
            # "worms_rec_error",
            # "worms_lsid",
        ]

    def create_translate_file(self):
        """ """
        self.import_taxa_worms()
        self.import_translate_to_worms()

        out_data_rows = []

        indata_species = pathlib.Path(self.data_in_path, "indata_taxa_by_name.txt")
        if indata_species.exists():
            print("Importing file: ", indata_species)
            with indata_species.open(
                "r", encoding="cp1252", errors="ignore"
            ) as indata_file:
                header = None
                for row in indata_file:
                    row = [item.strip() for item in row.strip().split("\t")]
                    if row:
                        if header is None:
                            header = row
                        else:
                            row_dict = dict(zip(header, row))
                            dyntaxa_scientific_name = row_dict.get("scientific_name", "")
                            dyntaxa_id = row_dict.get("dyntaxa_id", "")

                            scientific_name = dyntaxa_scientific_name
                            if scientific_name in self.translate_to_worms_dict:
                                translate_dict = self.translate_to_worms_dict[scientific_name]
                                scientific_name = translate_dict.get("scientific_name_to", "")

                            if len(scientific_name) >= 2:
                                row = [dyntaxa_scientific_name, dyntaxa_id]
                                if scientific_name in self.taxa_worms_dict:
                                    worms_dict = self.taxa_worms_dict[scientific_name]

                                    for column in self.translate_dyntaxa_to_worms_header[2:]:
                                        worms_column = self.rename_worms_header_items.get(column, column)
                                        row.append(worms_dict.get(worms_column, ""))
                                    out_data_rows.append(row)
                                else:
                                    print("- MISSING TAXA IN WORMS: ", scientific_name)
                            else:
                                print("- MISSING SCIENTIFIC NAME: ", dyntaxa_scientific_name, " - ", scientific_name)

            print("")


        # Write to file.
        outdata_path = pathlib.Path(self.data_out_path)
        if not outdata_path.exists():
            outdata_path.mkdir(parents=True)
        translate_file = pathlib.Path(outdata_path, "translate_dyntaxa_to_worms.txt")
        with translate_file.open("w", encoding="cp1252") as out_file:
            out_file.write("\t".join(self.translate_dyntaxa_to_worms_header) + "\n")
            for row in out_data_rows:
                out_file.write("\t".join(row) + "\n")


    def import_taxa_worms(self):
        """ """
        taxa_worms = pathlib.Path(self.data_out_path, "taxa_worms.txt")
        if taxa_worms.exists():
            print("Importing file: ", taxa_worms)
            with taxa_worms.open(
                "r", encoding="cp1252", errors="ignore"
            ) as indata_file:
                header = None
                for row in indata_file:
                    row = [item.strip() for item in row.strip().split("\t")]
                    if header is None:
                        header = row
                    else:
                        row_dict = dict(zip(header, row))
                        scientific_name = row_dict.get("scientific_name", "")
                        aphia_id = row_dict.get("aphia_id", "")
                        if scientific_name:
                            self.taxa_worms_dict[scientific_name] = row_dict

    def import_translate_to_worms(self):
        """ """
        translate_to_worms = pathlib.Path(self.data_out_path, "translate_to_worms.txt")
        if translate_to_worms.exists():
            print("Importing file: ", translate_to_worms)
            with translate_to_worms.open(
                "r", encoding="cp1252", errors="ignore"
            ) as indata_file:
                header = None
                for row in indata_file:
                    row = [item.strip() for item in row.strip().split("\t")]
                    if header is None:
                        header = row
                    else:
                        row_dict = dict(zip(header, row))
                        scientific_name = row_dict.get("scientific_name_from", "")
                        aphia_id = row_dict.get("aphia_id", "")
                        if scientific_name:
                            self.translate_to_worms_dict[scientific_name] = row_dict


if __name__ == "__main__":
    """ """
    taxa_mgr = CreateTranslateDyntaxaToWorms(
        data_in_path="data_in", data_out_path="data_out"
    )
    taxa_mgr.create_translate_file()
