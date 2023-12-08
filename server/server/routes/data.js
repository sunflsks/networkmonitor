let express = require('express');
let router = express.Router();
const { pool } = require('../db/db');

Date.prototype.toSQLRepresentation = function () {
  return this.toISOString().replace('T', ' ').replace('Z', '');
}

/* GET home page. */
router.get('/', function (req, res, next) {
  // open sqlite database and query for latitude, longitude, and rssi. then send over as JSON
  ts = new Date(parseInt(req.query.timestamp));
  if (isNaN(ts.getTime())) {
    ts = new Date();
    ts.setHours(ts.getHours() - 2);
  }

  pool.query("SELECT coordinates, rssi, timestamp FROM results WHERE timestamp > $1", [ts.toSQLRepresentation()], function (err, rows) {
    if (err) {
      console.log(err);
      res.status(500).send("Error querying database");
    } else {
      data_to_send = rows["rows"];
      console.log(`Sending ${data_to_send.length} rows to ${req.ip}`);
      res.json(data_to_send);
    }
  });
});

module.exports = router;
