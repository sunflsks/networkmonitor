/* global L */

const d3 = require('d3/dist/d3')
require('leaflet')
require('d3-hexbin/build/d3-hexbin.min')
require('d3-color/dist/d3-color.min')
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
  duration: 500
}

// nested array with following format:
// [[light green to dark green], [light red to dark red], [light blue to dark blue], [light orange to dark orange]]
const colorRanges =
  [['#cefad0', '#008631'],
    ['#ffcccb', '#ff0000'],
    ['#b3c6ff', '#0000ff'],
    ['#ffebcc', '#ff6600']]

const hexLayersForProvider = {}

const legend = L.control({ position: 'bottomleft' })
legend.onAdd = function (map) {
  const div = L.DomUtil.create('div', 'info legend')

  const grades = [-85, -75, -65]

  // eslint-disable-next-line comma-dangle
  for (const [provider,] of Object.entries(hexLayersForProvider)) {
    const colorScale = hexLayersForProvider[provider].colorScale()
    const providerLabel = document.createElement('label')
    providerLabel.innerHTML = provider

    div.appendChild(providerLabel)
    div.appendChild(document.createElement('br'))

    for (let i = 0; i < grades.length; i++) {
      const label = document.createElement('label')
      label.innerHTML = `<i style="background:${colorScale(grades[i])}"></i> ${grades[i]} ${grades[i + 1] ? ' to ' + grades[i + 1] : '+'}`
      div.appendChild(label)
      div.appendChild(document.createElement('br'))
    }

    div.appendChild(document.createElement('br'))
  }
  return div
}

const toggles = L.control({ position: 'bottomright' })
toggles.onAdd = function (map) {
  const div = L.DomUtil.create('div', 'info toggles')
  for (const [provider, layer] of Object.entries(hexLayersForProvider)) {
    console.log(`toggle for provider ${provider}`)
    const label = document.createElement('label')
    label.innerHTML = provider
    const input = document.createElement('input')
    input.type = 'checkbox'
    input.checked = true
    input.onchange = function () {
      if (input.checked) {
        layer.addTo(map)
      } else {
        map.removeLayer(layer)
      }
    }
    label.appendChild(input)
    div.appendChild(label)
    div.appendChild(document.createElement('br'))
  }
  return div
}

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
      let newProvider = false
      data.forEach(function (d) {
        if (d.coordinates.x == null || d.coordinates.y == null || d.provider == null) { return }
        if (hexLayersForProvider[d.provider] === undefined) {
          newProvider = true

          const newOptions = Object.assign({}, options)

          newOptions.colorDomain = [-85, -65]
          newOptions.colorRange = colorRanges.shift()

          hexLayersForProvider[d.provider] = L.hexbinLayer(newOptions).addTo(map)
          hexLayersForProvider[d.provider]
            .radiusValue(function (d) { return d.length })
            .radiusRange([6, 11])
            .lng(function (d) { return d[1] })
            .lat(function (d) { return d[0] })
            .colorValue(function (d) { return d[0].o[2] })
        }

        if (newProvider) {
          console.log('new provider')
          legend.addTo(map)
          toggles.addTo(map)
          newProvider = false
        }

        const latitude = d.coordinates.x
        const longitude = d.coordinates.y
        d.rssi = parseInt(d.rssi)
        toadd.push({ latitude, longitude, rssi: d.rssi, provider: d.provider })
      })

      if (toadd.length > 0) {
        const pointsForProviders = {}
        for (const point of toadd) {
          if (pointsForProviders[point.provider] === undefined) {
            pointsForProviders[point.provider] = []
          }

          pointsForProviders[point.provider].push([point.latitude, point.longitude, point.rssi])
        }

        for (const provider in pointsForProviders) {
          const hexLayer = hexLayersForProvider[provider]
          const points = pointsForProviders[provider]
          hexLayer.data(points)
        }
      }
    })
}

map.on('moveend', updateMap)

// On page load, download data once
updateMap({ type: 'load' })
