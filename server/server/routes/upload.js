const express = require('express')
const router = express.Router()
const { pool } = require('../db/db')

router.use(express.json())

// Test route
router.get('/', function (req, res, next) {
  res.send('POST with json body to /upload')
})

router.post('/', async (req, res) => {
  const data = req.body // Array of objects
  const device = data.device
  const points = data.points

  console.log(`Received upload request from ${req.headers['x-forwarded-for'] || req.socket.remoteAddress}`)

  console.log(data)
  // data validation !!!
  // Function to transform and insert data
  const insertData = async (data) => {
    try {
      const query = `
        INSERT INTO results (timestamp, ip_address, latency, rssi, packet_dropped, coordinates, device, provider)
        VALUES ($1, $2, $3, $4, $5, point($6, $7), $8, $9)
      `

      for (const item of points) {
        console.log(`point ${item.timestamp} inserted at ${item.gpsinfo.latitude}, ${item.gpsinfo.longitude}`)
        const values = [
          new Date(item.timestamp),
          item.ip_address,
          item.latency,
          item.rssi,
          item.packet_dropped,
          item.gpsinfo.latitude,
          item.gpsinfo.longitude,
          device,
          item.provider
        ]
        await pool.query(query, values)
      }
    } catch (err) {
      console.error('Error during database operation', err)
      throw err
    }
  }

  try {
    await insertData(data)
    res.status(200).send('Data inserted successfully')
  } catch (err) {
    console.log(err)
    res.status(500).send('Failed to insert data')
  }
})

module.exports = router
