const express = require('express')
const router = express.Router()
const { pool } = require('../db/db')

function dateToSQLRepresentation (date) {
  return date.toISOString().replace('T', ' ').replace('Z', '')
}

/* GET home page. */
router.get('/', function (req, res, next) {
  const swlat = parseFloat(req.query.swlat)
  const swlng = parseFloat(req.query.swlng)
  const nelat = parseFloat(req.query.nelat)
  const nelng = parseFloat(req.query.nelng)

  let ts = new Date(parseInt(req.query.timestamp))
  if (isNaN(ts.getTime())) {
    ts = new Date()
    ts.setHours(ts.getHours() - 2)
  }

  console.log(ts)

  pool.query('SELECT coordinates, rssi, timestamp, provider FROM results WHERE timestamp > $1 AND (coordinates <@ box(point($2, $3),point($4, $5)))', [dateToSQLRepresentation(ts), nelat, nelng, swlat, swlng], function (err, rows) {
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
