# Upload CSV Tool
This tool is for uploading data from a CSV file to Optimum Core

## Set up

1. Install Python 3
1. pip intsall json, requests, datetime and csv

1. Set these environment variables:
    * TESLA_USER
    * TESLA_PASSWORD
    
1. Create csv file
    - header row = "Timestamp", "[PointId]"
    - rows = timestamp, value
    
    Example:
    ```
    timestamp,77622668-061e-4c85-b81d-439af8495adb
    2020-05-06 09:00,0.0
    2020-05-06 09:05,0.0
    2020-05-06 09:10,0.0
    .
    .
    .
    ```



    
## To Run the Tool
1. Run python uploadcsv.py [api_domain] [csv_file_path]

example:

python uploadcsv.py api.optimumenergyco.com /Users/hwilkinson/Desktop/before_divide.csv
