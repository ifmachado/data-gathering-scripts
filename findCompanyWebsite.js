//Dependencies

require('dotenv').config();
var fs = require('fs');
const prompt = require('prompt-sync')();
const clearbit = require('clearbit');

//Definitions

// Read CSV file
function readCSVFile(fileName, offset=0) {
  var myData = fs.readFileSync(fileName, 'utf8');
  var rows = myData.split('\r\n');
  rows.shift(); //Remove header

  if (offset != 0){
    rows = rows.map(row => {
      const columns = row.split(',');
      return columns[offset]; // Extract the selected column only
      }
    )
  }
  return rows
}

// Write data to CSV file
function writeCSVFile(headers, data, outputName) {
  for (let i = 0; i < data.length; i++) {
    headers += data[i].join(",") + "\n";
  }
  fs.writeFile(outputName, headers, function (err) {
    if (err) throw err;
  });
}

function retrieveURLsFromClearbit(companies, key) {
  const clearbitClient = clearbit(key);
  const NameToDomain = clearbitClient.NameToDomain;
  var compNameandURL = [];
  var promises = [];

  for (let i = 0; i < companies.length; i++) {
    const promise = NameToDomain.find({ name: companies[i] })
      .then(function (result) {
        compNameandURL.push([companies[i], result.domain]);
      })
      .catch(NameToDomain.NotFoundError, function (err) {
        compNameandURL.push([companies[i], "not found"]);
      })
      .catch(function (err) {
        console.log(err);
      });

    promises.push(promise);
  }

  return Promise.all(promises)
    .then(function () {
      console.log("Retrieving URLs...");
      return compNameandURL;
    })
    .catch(function (err) {
      console.log('An error occurred while processing requests:', err);
    });
}

// Main code

// Get file name and read CSV
const name = prompt('Enter file name: ');
const compNames = readCSVFile(name);

// Used for local testing so key don't have to be entered every time
// const key = process.env.CLEARBIT_KEY

// Get Clearbit key
const key = prompt('Enter Clearbit key: ');

// Retrieve URLs from Clearbit Name to Domain API
retrieveURLsFromClearbit(compNames, key)
  .then(function (compNameandURL) {
    // Write Name and Domain to CSV
    writeCSVFile("Company,Domain\n", compNameandURL, "companies.csv");
    console.log("Companies.csv written successfully.")
  })
  .catch(function (err) {
    console.log('An error occurred:', err);
  });