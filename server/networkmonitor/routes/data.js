var express = require('express');
var sqlite = require('sqlite3');
var router = express.Router();

const DB_PATH="/usr/local/share/ping_results.db";

/* GET home page. */
router.get('/', function(req, res, next) {
  // open sqlite database and query for latitude, longitude, and rssi. then send over as JSON
  var db = new sqlite.Database(DB_PATH);
  db.all("SELECT latitude, longitude, rssi FROM results", function(err, rows) {
    if (err) {
      console.log(err);
      res.status(500).send("Error querying database");
    } else {
      res.json(rows);
    }
  });
});

module.exports = router;
