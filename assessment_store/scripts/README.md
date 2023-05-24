# 📜 Scripts

### Import from application.

To import all the application jsons from the application store for a specific `round_id` you run (from project root):

        python -m scripts.import_from_application --roundid={your round id} --app_type={your application type (e.g COFR2W2)}


### populate_location_data script does the following

1. Extracts postcode from the 'address of asset' field in the application form
1. Sends these postcodes to postcodes.io to retrieve further location information, eg. country
1. Updates the database, populating `assessment_records.location_json_blob` with a json blob containing the location details
1. Writes the retrieved location data out to a csv file at the specified location.

To run locally:

        python -m scripts.populate_location_data --fund_id 47aef2f5-3fcb-4d45-acb5-f0152b5f03c4 --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --update_db True --write_csv True --csv_location ./locations.csv

To run on paas, execute the following (starts a task using the app context etc)

        cf run-task funding-service-design-assessment-store-dev --command "python -m scripts.populate_location_data --fund_id 47aef2f5-3fcb-4d45-acb5-f0152b5f03c4 --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --update_db True --write_csv True --csv_location /tmp/locations.csv && cat /tmp/locations.csv" --name populate_location

The `cat /tmp/locations.csv` prints out the csv to the logs so we can copy/paste to send to the assessors if needed (we cannot access the file system of the container spun up to run this on paas).

If there is data in your docker DB, you can also execute this script locally in the container:

        docker exec -ti <assessment_store_container_id> scripts/populate_location_data.py --fund_id 47aef2f5-3fcb-4d45-acb5-f0152b5f03c4 --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --update_db True --write_csv False


### export_assessment_data script does the following:

The process_assessment_data function performs the processing of assessment data for a given fund round. It takes the following parameters:

- round_id: The UUID of the round for the fund.
- write_csv: A boolean indicating whether to export the data to a CSV file.
- csv_location: The location to save the CSV file (optional if write_csv is False).

During processing, the function retrieves assessment data for the specified round_id using the get_assessment_records_by_round_id function. It then proceeds to extract the requested data for the round.

To run locally

        python -m scripts.export_assessment_data --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd True --write_csv True --csv_location ./assessment_data.csv

If there is data in your docker DB, you can also execute this script locally in the container

        docker exec -ti b1afa47afbd5 scripts/export_assessment_data.py --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --write_csv True --csv_location file_location.csv

**To run on paas, execute the following steps**
*Note: Choose the app based on your specific environment. The following example pertains to the test environment.*

1. Before running the task, make sure you're recording the logs and and DO NOT change the file name `tail.txt`

        cf logs funding-service-design-assessment-store-test | tee ~/tail.txt

1. In a new terminal window, run task as usual, give it a unique --name and DO NOT change the file name `assessment_data.csv`

        cf run-task funding-service-design-assessment-store-test --command "python -m scripts.export_assessment_data --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --write_csv True --csv_location /tmp/assessment_data.csv && cat /tmp/assessment_data.csv" --name export_assessment_data

1. Wait for the logs to finish, ends at `destroying container for instance`, and Ctrl + C command on the terminal window running the cf logs to save the file.
1. Next, execute the "sed" command to eliminate unnecessary logs.

if you are on Windows sub system for Linux or Linux run the following command:

        sed -e 's/.*] OUT//' -e '0,/Exit/I!d' -e 's/Exit.*//;/^$/d' -e '/Retrieving/,/\/tmp\/assessment_data.csv/d' ~/tail.txt > ~/final.csv

If you are on Mac, run the following command:


        sed -e 's/.*] OUT//' -e 's/Exit.*//;/^$/d' -e '/Retrieving/,/\/tmp\/assessment_data.csv/d' ~/tail.txt > ~/final.csv

*Please note this command leaves two trailing lines at the end of the file which look like this and they can be deleted manually:*

        Cell 9bc96142-b9d9-435a-8dd0-723da2db27c7 stopping instance a08d8872-3035-44cc-a109-07842236fed6
        Cell 9bc96142-b9d9-435a-8dd0-723da2db27c7 destroying container for instance a08d8872-3035-44cc-a109-07842236fed6


1. `final.csv` will be located in the /home/<name of user> directory on the local machine, otherwise known as ~/  - alternatively, you can direct `final.csv` wherever you like, as long as you know the directory structure. ~/ will be the easiest to locate for both Macs and PCs.
