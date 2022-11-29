# Species

Python code used to keep marine monitoring species lists in sync with 
WoRMS, World Register of Marine Species (http://www.marinespecies.org/).

The WoRMS REST webservice (http://www.marinespecies.org/rest/) is used to access WoRMS.

## Installation

Check that Python3, venv and git are installed. Create a directory for the code. Start a terminal window.

    git clone https://github.com/sharkdata/species-worms.git
    cd species-worms
    python -m venv venv
    source venv/bin/activate # On Windows "venv\Scripts\activate".
    pip install -r requirements.txt # Not required if empty.

## Usage

Edit the file **data_in/indata_taxa_by_name.txt**.

Add scientific names for the species you want to have in your list.
Higher taxa will be automatically generated based on the classification for
each taxa in the list.

If there are problems with homonyms there is a possibility to add AphiaId.
Use the file **data_in/indata_taxa_by_aphia_id.txt**.

Run the command:
    # On Linux:
    source venv/bin/activate 
    # On Windows:
    venv\Scripts\activate

    python extract_taxa_from_worms_main.py

Check the files in **data_out**. You will find some tab delimited text files (that easily 
can be opened in Excel or LibreOffice Calc):

- **taxa_worms.txt**   Contains information for each taxa and parent taxa.

- **translate_to_worms.txt**   If the species in the indata list is not valid any longer, the will appear here and translated to the valid taxa.

- **errors.txt**   Contains info about species that couldn't be included automatically. There are two main reasons: Error code 204 = "not found" and error code 206 = "multiple alternatives was found".

To fix the errors, you have to check out valid AphiaID (http://www.marinespecies.org/aphia.php?p=search) for each species and add them manually to the file **data_in/indata_taxa_by_aphia_id.txt**.

There is a small database file used as a cache to speed up if the same taxa is checked multiple times.
The cache is stored in the file **worms_cache.db**. Remove that file if you don't want to use the cached results.

## Contact info

- shark@smhi.se
