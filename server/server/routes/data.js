const express = require('express')
const router = express.Router()
const { pool } = require('../db/db')

function dateToSQLRepresentation (date) {
  return date.toISOString().replace('T', ' ').replace('Z', '')
}

/* GET home page. */
router.get('/', function (req, res, next) {
  // open sqlite database and query for latitude, longitude, and rssi. then send over as JSON
  let ts = new Date(parseInt(req.query.timestamp))
  if (isNaN(ts.getTime())) {
    ts = new Date()
    ts.setHours(ts.getHours() - 2)
  }

  pool.query('SELECT coordinates, rssi, timestamp FROM results WHERE timestamp > $1', [dateToSQLRepresentation(ts)], function (err, rows) {
    if (err) {
      console.log(err)
      res.status(500).send('Error querying database')
    } else {
      const dataToSend = rows.rows
      console.log(`Sending ${dataToSend.length} rows to ${req.ip}`)
      res.json(dataToSend)
    }
  })
})

module.exports = router
