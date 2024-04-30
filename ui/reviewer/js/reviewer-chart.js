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
    const skewList = [];
    oneYearArray.forEach(line => {
        if (line.middleValue > 655000) {
            skewList.push(Number(line.property_count));
        } else {
            xAxis.push(line.middleValue);
            yAxis.push(Number(line.property_count));
        }
    });
    console.log(skewList);
    const sumSkew = skewList.reduce((a, b) => a + b);
    xAxis.push('More than 655000');
    yAxis.push(sumSkew);
    return [xAxis, yAxis];
}

function distributionChart(xValue, yValue) {
  const options = {
    chart: {
      id: "distribution-chart",
      height: 270,
      type: "area",
      foreColor: "#404040", // color of the text
      toolbar: {
        autoSelected: "pan",
        show: true,
      },
    },
    dataLabels: {
      enabled: false,
    },
    title: {
      text: "Tax Year Assessment Value Distribution",
      align: 'left',
      margin: 10,
      offsetX: 0,
      offsetY: 0,
      floating: false,
      style: {
        fontSize:  '16px',
        fontWeight:  'bold',
        fontFamily:  'sans-serif',
        color:  '#404040',
      },
    },
    series: [
      {
        name: "Count of Properties",
        data: yValue,
      },
    ],
    tooltip: {
      x: {
        show: false,
      },
      marker: {
        show: false,
      },
    },
    colors: ['#5176E1'], // color of the popup
    fill: {
      type: "gradient",
      gradient: {
        shadeIntensity: 1,
        type: "horizontal",
        colorStops: [
          {
            offset: 0,
            color: '#5176E1',
            opacity: 0.7,
          },
          {
            offset: 15,
            color: '#6BA9E1',
            opacity: 0.7,
          },
          {
            offset: 30,
            color: '#98DBD6',
            opacity: 0.7,
          },
          {
            offset: 50,
            color: '#E0B853',
            opacity: 0.7,
          },
          {
            offset: 70,
            color: '#E18A5B',
            opacity: 0.7,
          },
          {
            offset: 100,
            color: '#E1544F',
            opacity: 0.7,
          },
        ],
      },
    },
    stroke: {
      width: 1,
    },
    yaxis: {
        min: 0,
        tickAmount: 4,
    },
    xaxis: {
      categories: xValue,
      tickAmount: 15,
      labels: {
        formatter: function (value) {
          return "$" + value;
        },
      },
    },
  };

  const chart = new ApexCharts(document.querySelector(".distribution-chart"), options);

  return chart;
}

function getYearList(minYear, maxYear) {
  const yearList = [];
  for (let i = minYear; i < maxYear; i++) {
    yearList.push(i.toString());
  }
  return yearList;
}

function handleYearDropdown(dropdown, yearList, maxYear) {
  // create default option that select the current year
  const defaultOption = document.createElement('option');
  defaultOption.value = 'default';
  defaultOption.text = maxYear.toString();
  dropdown.appendChild(defaultOption);
  // other options
  for (let i = 0; i < yearList.length; i++) {
    const option = document.createElement('option');
    option.value = yearList[i];
    option.text = yearList[i];
    dropdown.appendChild(option);
  }
}

export {
    getYearData,
    getArrayForChart,
    distributionChart,
    getYearList,
    handleYearDropdown,
};