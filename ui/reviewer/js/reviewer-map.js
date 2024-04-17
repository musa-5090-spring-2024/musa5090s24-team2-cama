const url = 'https://storage.googleapis.com/musa509s23_team02_public/tiles/properties/{z}/{x}/{y}.pbf';

function initializeMap() {
  const map = L.map('map', { zoomSnap: 0, maxZoom: 20, minZoom: 12 }).setView([39.99, -75.15], 12); // zoomSnap 0 make the zoom level to real number
  const baseTileLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
  });
  baseTileLayer.addTo(map);

  const vectorTileOptions = {
    rendererFactory: L.canvas.tile,
    attribution: 'Something',
    vectorTileLayerStyles: {
      // A plain set of L.Path options.
      'property_tile_info': function (properties) {
        if (properties.current_assessed_value < 160000) {
          return {
            weight: 0,
            fillColor: '#5176E1',
            fillOpacity: 1,
            fill: true,
          };
        }

        if (properties.current_assessed_value < 250000 && properties.current_assessed_value >= 160000) {
          return {
            weight: 0,
            fillColor: '#6BA9E1',
            fillOpacity: 1,
            fill: true,
          };
        }

        if (properties.current_assessed_value < 400000 && properties.current_assessed_value >= 250000) {
          return {
            weight: 0,
            fillColor: '#98DBD6',
            fillOpacity: 1,
            fill: true,
          };
        }

        if (properties.current_assessed_value < 1000000 && properties.current_assessed_value >= 400000) {
          return {
            weight: 0,
            fillColor: '#E0B853',
            fillOpacity: 1,
            fill: true,
          };
        }

        if (properties.current_assessed_value < 4500000 && properties.current_assessed_value >= 1000000) {
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
      // A function for styling features dynamically, depending on their
      // properties and the map's zoom level
      // admin: function(properties, zoom) {
      //   var level = properties.admin_level;
      //   var weight = 1;
      //   if (level == 2) {weight = 4;}
      //   return {
      //       weight: weight,
      //       color: '#cf52d3',
      //       dashArray: '2, 6',
      //       fillOpacity: 0
      //   }
      // },
      // A function for styling features dynamically, depending on their
      // properties, the map's zoom level, and the layer's geometry
      // dimension (point, line, polygon)
      // 'property_tile_info': function(properties, zoom, geometryDimension) {
      // if (geometryDimension === 1) {   // point
      //   return ({
      //     radius: 5,
      //     color: '#cf52d3',
      //   });
      // }

      // if (geometryDimension === 2) {   // line
      //   return ({
      //     weight: 1,
      //     color: '#cf52d3',
      //     dashArray: '2, 6',
      //     fillOpacity: 0,
      //   });
      // }

      // if (geometryDimension === 3) {   // polygon
      //   return ({
      //     weight: 1,
      //     fillColor: '#9bc2c4',
      //     fillOpacity: 1,
      //     fill: true,
      //   });
      // }
      // },
      // An 'icon' option means that a L.Icon will be used
      // place: {
      //   icon: new L.Icon.Default(),
      // },
      // road: [],
    },
  };

  L.vectorGrid.protobuf(url, vectorTileOptions).addTo(map);

    //cross origin resource sharing (CORS)

    return map;
}

export {
    initializeMap,
};
