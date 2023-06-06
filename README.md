USES:

FindCompanyWebsite script uses Clearbit API to get companies websites based on Company name.
CrossReferenceScript script uses PeopleDataLabs API to get company data (industry and location) using websites obtained on FindCompanyWebsite script to cross-reference the data obtained.
Crossreferencing may be necessary as different companies may have the same name.


SET UP:

1. Install Python: https://www.python.org/downloads/

2. Install Node: https://nodejs.org/en/download

3. Create free account with Clearbit: https://dashboard.clearbit.com/signup

4. Get Clearbit API key: https://help.clearbit.com/hc/en-us/articles/6045527495191-Where-Can-I-Find-My-API-Key-

5. Create free account with PeopleDataLabs and get API Key: https://docs.peopledatalabs.com/docs/quickstart#create-an-account

PS: save all API keys in a file you can access later.

6. Open scripts directory in Terminal:

	** With File Explorer open on the directory with all the scripts, right click on an empty space.
	Choose the option Open in Terminal. **

7. Install FindCompanyWebsite.js dependencies => run the following command: npm install

8. Install CrossReferenceScript.py dependencies => run the following command: pip install -r requirements.txt

CSV SPECS:
* must have only one column (with the company names)
* must have a header (otherwise, it will skip the company on the first line)
* must be saved in the same directory as the scripts

RUN

1. Open scripts directory in Terminal (see above)

2. To run FindCompanyWebsite script, paste the command: node findCompanyWebsite.js

3. To run CrossReferenceScript, paste the command: Python crossReferenceScript.py 
