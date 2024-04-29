/* globals Papa */

import { initializeMap } from './reviewer-map.js';
import { getYearData, getArrayForChart, distributionChart } from './reviewer-chart.js';

const distributionChartUrl = 'https://storage.googleapis.com/musa5090s24_team02_public/tax_year_assessment_bins/tax_year_assessment_bins.csv';

// This is the same as the function below

// async function downloadData(onSuccess, onFailure) {
//     const resp = await fetch(distributionChartUrl);
//     if (resp.status === 200) {
//         const data = await resp.json();
//         onSuccess(data);
//     } else {
//         alert('Oh no, I failed to download the data.');
//         if (onFailure) { onFailure() }
//     }
// }

// downloadData(smurf => console.log(smurf));

// function downloadData(onSuccess, onFailure) { // onSuccess, onFailure are both place holders for functions
//     fetch(distributionChartUrl)
//     .then(resp => {
//       if (resp.status === 200) {
//         const data = resp.json();
//         return data;
//       } else {
//         alert('Oh no, I failed to download the data.');
//         if (onFailure) { onFailure() }
//       }
//     })
//     .then(onSuccess);
// }


Papa.parse(distributionChartUrl, {
	download: true,
	header: true, // Assuming the CSV has headers
    complete: function(results) {
        // results.data contains the parsed CSV data as an array of objects
        const data = results.data;
        console.log(data);
        const oneYearArray = getYearData(data, "2023");
        console.log(oneYearArray);
        const [xValue, yValue] = getArrayForChart(oneYearArray);
        distributionChart(xValue, yValue);
    },
});

window.map = initializeMap();