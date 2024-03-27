function initializeMap() {
    const map = L.map('map', { zoomSnap: 0 }).setView([39.99, -75.15], 11); // zoomSnap 0 make the zoom level to real number
    const baseTileLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
        maxZoom: 19,
    });
    baseTileLayer.addTo(map);

    return map;
}

export {
    initializeMap,
};
