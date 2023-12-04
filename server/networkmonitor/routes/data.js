var express = require('express');
var sqlite = require('sqlite3');
var router = express.Router();

const DB_PATH = "/usr/local/share/ping_results.db";

/* GET home page. */
router.get('/', function (req, res, next) {
  // open sqlite database and query for latitude, longitude, and rssi. then send over as JSON
  ts = new Date(parseInt(req.query.timestamp)) ?? new Date().setHours(new Date().getHours() - 2);
  var db = new sqlite.Database(DB_PATH);
  db.all("SELECT latitude, longitude, rssi, timestamp FROM results WHERE timestamp > ?", [ts.toISOString()], function (err, rows) {
    if (err) {
      console.log(err);
      res.status(500).send("Error querying database");
    } else {
      console.log(`Sending ${rows.length} rows to ${req.ip}`);
      res.json(rows);
    }
  });
});

module.exports = router;
