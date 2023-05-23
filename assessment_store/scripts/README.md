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


### extract_assessment_data script does the following:

The process_assessment_data function performs the processing of assessment data for a given fund round. It takes the following parameters:

- round_id: The UUID of the round for the fund.
- write_csv: A boolean indicating whether to export the data to a CSV file.
- csv_location: The location to save the CSV file (optional if write_csv is False).

During processing, the function retrieves assessment data for the specified round_id using the get_assessment_records_by_round_id function. It then proceeds to extract the requested data for the round.

To run locally:

        python -m scripts.export_application_data --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd True --write_csv True --csv_location ./locations.csv

To run on paas, execute the following (starts a task using the app context etc)

        cf run-task funding-service-design-assessment-store-dev --command "python -m scripts.export_application_data --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --write_csv True --csv_location /tmp/locations.csv && cat /tmp/locations.csv" --name populate_location

The `cat /tmp/locations.csv` prints out the csv to the logs so we can copy/paste to send to the assessors if needed (we cannot access the file system of the container spun up to run this on paas).

If there is data in your docker DB, you can also execute this script locally in the container:

        docker exec -ti b1afa47afbd5 scripts/export_application_data.py --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --write_csv True --csv_location file_location.csv
