require('leaflet');
require('d3/dist/d3')
require('d3-hexbin/build/d3-hexbin.min')
require('./js/leaflet-d3')

// Creates a leaflet map binded to an html <div> with id "map"
// setView will set the initial map view to the location at coordinates
// 13 represents the initial zoom level with higher values being more zoomed in
var map = L.map('map', {center: [32.906950, -96.950270], zoom: 15})

// Adds the basemap tiles to your web map
// Additional providers are available at: https://leaflet-extras.github.io/leaflet-providers/preview/
var osm_mapnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; OSM Mapnik <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var options = {
    radius : 12,
    opacity: 1,
    duration: 500,
	colorRange: [ '#660000', '#5af019']
};

var hexLayer = L.hexbinLayer(options).addTo(map)

var rssiToColorValue = function(rssi) {
	if (rssi > -65) { return 5; }
	if (rssi > -75) { return 4; }
	if (rssi > -85) { return 3; }
	if (rssi > -95) { return 4; }
	return 1;
};

hexLayer
  .radiusRange([6, 11])
  .lng(function(d) { return d[1]; })
  .lat(function(d) { return d[0]; })
  .colorValue(function(d, i) {
	 	const rssi = d[0].o[2];
		console.log(rssi)
		return rssiToColorValue(rssi);
 	})
  .radiusValue(function(d) { return d.length; });

setTimeout(function() {
	fetch('http://localhost:3000/data')
	.then(response => response.json())
	.then(data => {
	  toadd = []
	  data.forEach(function(d) {
		if (d.latitude == null || d.longitude == null)
		  return;
		d.rssi = parseInt(d.rssi);
		toadd.push([d.latitude, d.longitude, d.rssi]);
	  });

	  hexLayer.data(toadd).addTo(map);
	});
}, 10000);