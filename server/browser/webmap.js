/* global L */

require('leaflet')
require('d3/dist/d3')
require('d3-hexbin/build/d3-hexbin.min')
require('./leaflet-d3')

// Creates a leaflet map binded to an html <div> with id "map"
// setView will set the initial map view to the location at coordinates
// 13 represents the initial zoom level with higher values being more zoomed in
const map = L.map('map', { center: [32.906950, -96.950270], zoom: 15 })

// Adds the basemap tiles to your web map
// Additional providers are available at: https://leaflet-extras.github.io/leaflet-providers/preview/
L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OSM Mapnik <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map)

const options = {
  radius: 12,
  opacity: 1,
  duration: 500,
  colorRange: ['darkred', 'green']
}

const hexLayer = L.hexbinLayer(options).addTo(map)

const rssiToColorValue = function (rssi) {
  if (rssi > -65) { return 5 }
  if (rssi > -75) { return 4 }
  if (rssi > -85) { return 3 }
  if (rssi > -95) { return 4 }
  return 1
}

hexLayer
  .radiusRange([6, 11])
  .lng(function (d) { return d[1] })
  .lat(function (d) { return d[0] })
  .colorValue(function (d, i) {
    const rssi = d[0].o[2]
    return rssiToColorValue(rssi)
  })
  .radiusValue(function (d) { return d.length })

// Set initial date to beginning of time

function updateMap (e) {
  console.log(`Event handler called with event type: ${e.type}`)
  // Get the current map bounds
  const bounds = map.getBounds()

  // Extract corners from bounds
  const sw = bounds.getSouthWest()
  const ne = bounds.getNorthEast()

  // Construct the URL to call
  const url = `${location.origin}/data?swlat=${sw.lat}&swlng=${sw.lng}&nelat=${ne.lat}&nelng=${ne.lng}&timestamp=0`

  // Fetch the data from the server
  fetch(url)
    .then(response => response.json())
    .then(data => {
      const toadd = []
      data.forEach(function (d) {
        if (d.coordinates.x == null || d.coordinates.y == null) { return }
        const latitude = d.coordinates.x
        const longitude = d.coordinates.y
        d.rssi = parseInt(d.rssi)
        toadd.push([latitude, longitude, d.rssi])
      })

      console.log(toadd)
      if (toadd.length > 0) {
        hexLayer.data(toadd).addTo(map)
      }
    })
}

map.on('moveend', updateMap)

// On page load, download data once
updateMap({ type: 'load' })
