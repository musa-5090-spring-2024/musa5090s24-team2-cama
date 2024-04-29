/* globals ApexCharts */

function getYearData(data, year) { // year is a string
    const oneYearArray = [];
    data.forEach(line => {
        if (line.tax_year === year) {
            line.middleValue = line.upper_bound - (line.upper_bound - line.lower_bound) / 2;
            oneYearArray.push(line);
        }
    });
    return oneYearArray;
}

function getArrayForChart(oneYearArray) {
    const xAxis = [];
    const yAxis = [];
    oneYearArray.forEach(line => {
        xAxis.push(line.middleValue);
        yAxis.push(Number(line.property_count));
    });
    return [xAxis, yAxis];
}

function distributionChart(xValue, yValue) {
    const options = {
        chart: {
          height: 250,
          type: "area",
        },
        dataLabels: {
          enabled: false,
        },
        series: [
          {
            name: "Count of Properties",
            data: yValue,
          },
        ],
        fill: {
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.9,
            stops: [0, 90, 100],
          },
        },
        xaxis: {
          categories: xValue,
        },
      };

    const chart = new ApexCharts(document.querySelector("#distribution-chart"), options);

    chart.render();
}

export {
    getYearData,
    getArrayForChart,
    distributionChart,
};