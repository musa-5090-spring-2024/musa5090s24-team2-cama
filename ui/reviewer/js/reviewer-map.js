const url = 'https://storage.googleapis.com/musa5090s24_team02_public/tiles/properties/{z}/{x}/{y}.pbf';

const assessRadio = document.getElementById("assessRadio");
const predictRadio = document.getElementById("predictRadio");

let styleProperty = 'current_assessed_value';

function getMapStyle(styleProperty) {
  const styleOptions = {
    // A plain set of L.Path options.
    'property_tile_info': (properties) => {

      if (properties[styleProperty] < 160000) {
        return {
          weight: 0,
          fillColor: '#5176E1',
          fillOpacity: 1,
          fill: true,
        };
      }

      if (properties[styleProperty] < 250000 && properties[styleProperty] >= 160000) {
        return {
          weight: 0,
          fillColor: '#6BA9E1',
          fillOpacity: 1,
          fill: true,
        };
      }

      if (properties[styleProperty] < 400000 && properties[styleProperty] >= 250000) {
        return {
          weight: 0,
          fillColor: '#98DBD6',
          fillOpacity: 1,
          fill: true,
        };
      }

      if (properties[styleProperty] < 1000000 && properties[styleProperty] >= 400000) {
        return {
          weight: 0,
          fillColor: '#E0B853',
          fillOpacity: 1,
          fill: true,
        };
      }

      if (properties[styleProperty] < 4500000 && properties[styleProperty] >= 1000000) {
        return {
          weight: 0,
          fillColor: '#E18A5B',
          fillOpacity: 1,
          fill: true,
        };
      }

      else {
        return {
          weight: 0,
          fillColor: '#E1544F',
          fillOpacity: 1,
          fill: true,
        };
      }
    },
  };

  return styleOptions;
}


function handleRadioSelection(vectordata) {
  assessRadio.addEventListener('click', () => {
    styleProperty = 'tax_year_assessed_value';
    console.log('clicked assess radio');
    vectordata.redraw();
  });

  predictRadio.addEventListener('click', () => {
    styleProperty = 'current_assessed_value';
    console.log('clicked assess radio');
    vectordata.redraw();
  });
}

function initializeMap() {
  const map = L.map('map', { zoomSnap: 0, maxZoom: 20, minZoom: 12 }).setView([39.99, -75.15], 12); // zoomSnap 0 make the zoom level to real number
  const baseTileLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
  });
  baseTileLayer.addTo(map);

  const vectorTileOptions = {
    rendererFactory: L.canvas.tile,
    attribution: 'Something',
    vectorTileLayerStyles: getMapStyle(styleProperty),
  };

  const vectordata = L.vectorGrid.protobuf(url, vectorTileOptions).addTo(map);
  window.vectordata = vectordata;

  handleRadioSelection(vectordata);

    //cross origin resource sharing (CORS)

  return map;
}



// vectordata.redraw();

export {
    initializeMap,
};
