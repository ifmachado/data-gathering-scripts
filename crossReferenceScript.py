import csv
import os
from dotenv import load_dotenv
from urllib.request import Request, urlopen
from peopledatalabs import PDLPY

# Used for local testing
# load_dotenv()
# key = os.getenv('PPLDATA_KEY')

# Get API key
key = input("Enter People Data Labs API key: ")
companies = []

# Read CSV
fileName = input("Enter CSV file name: ")
with open(fileName, newline='') as csvfile:
    spamReader = csv.reader(csvfile, delimiter=',', quotechar='|')

    # Remove header
    rowsList = list(spamReader)
    rowsList.pop(0)

    # Add only URLs from CSV to array
    for row in rowsList:
        str = ""
        companies.append(str.join(row[1]))

codeDict = {}

for company in companies:
    status = ""
    # Check if website found by Clearbit
    if company == "not found":
        codeDict[company] = "website not provided"
    else:  
    # Get cross referencing data from People Data Labs API
        client = PDLPY(
            api_key=key,
        )
        result = client.company.enrichment(
            website=company,
            pretty=True,
        ).json()

        #If found, add industry and location to dict
        if result['status'] == 200:
            # Some results don't return location, check for None results
            locationName = result['location']
            if locationName == None:
                locationName = "LocationUnavailable, , "
                codeDict[company] = (result['industry'] + "," +  locationName + ",")
            else:
                locationName = locationName['name'].replace(" ", "")
                codeDict[company] = (result['industry'] + "," +  locationName + ",")

        # Not found, add message to disct
        elif result['status'] == 404:
            codeDict[company] = (result['message'] + ", , , , ")
        # Error, print message to console
        else: 
            print(result['error']['message'])

        #Access URL and check if code 200. All others return code "error"
        fullAddress = "http://www." + company
        request_site = Request(fullAddress, headers={"User-Agent": "Mozilla/5.0"})
        try:
            code = urlopen(request_site).getcode()
            # Website opens
            if code == 200:
                status = "OK"

            # Website doesn't open
            else:
                status = "NO"

        # urlopen() error
        except:
            status = "error"

    # Append code to end of string value on dictionary
    codeDict[company] += status 

# Write dict with company data to csv
with open('crossreference.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
    spamwriter.writerow(['Website'] + ['Industry'] + ['City'] + ['State'] + ['Country'] + ['Opened?'])
    for key in codeDict.keys():
        spamwriter.writerow([key] + [codeDict[key]])
    print("Cross reference CSV saved succesfully.")