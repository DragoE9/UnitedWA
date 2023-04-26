# UnitedWA
A command-line python tool for the managing and monitoring of WA Voting Blocks in NationStates
## About
This project uses the pynationstates wraper, which much be installed (pip install nationstates) prior to use of this application. This application makes calls to the nationstates.net API. The username you provide will be given to the API as part of the UserAgent the program sends to identify itself to the API. This application uses pynationstates' built-in rate-limiter.
## Usage
Download the whole repository. All of the files are required to have the program work. Launch the app by running UnitedWA.py
## Commands
The following information is also available in-app by running the "help" command:
1. compliance - Checks the compliance of dossier regions with your WA recomendation. Export report as csv available.
2. region_add - Add a region to the observance dossier
3. region_del - Remove a region from the observance dossier
4. region_list - Lists all regions in the dossier
5. rec_update - Change the voting recomendations
6. power_refresh - Recalculates and updates regional voting powers
7. calc_vote - Calculates a WA vote recomendation based on the URA standard formula. Export report as csv available.
8. exit - exit
This program performs input standardisation meaning that nothing should be case-sensitive. The program can handle spaces in region names, but commands must use underscores.
## Advanced
This program uses csv files (regions.csv, recomendations.csv, votepower.csv) to store data, so it can be remembered the next time. These files must exist in the folder where the main program (UnitedWA.py) is located or else it won't work. It is not reccomended to edit these files directly. The program provides input standardisation and auto-formatting. If you do edit these files you must make sure they are in the correct format or else they won't work. The files provided have placeholder data, because some commands may cause crashes if run on empty files.
## Known Issues
None Currently
## Features to be added
None Currently
