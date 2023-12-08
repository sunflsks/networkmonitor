let express = require('express');
let router = express.Router();

// Test route
router.get('/', function(req, res, next) {
  res.send("Hello World!");
});

module.exports = router;