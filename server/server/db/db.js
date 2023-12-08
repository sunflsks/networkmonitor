const { Pool } = require('pg');
const { USERNAME, PASSWORD } = require('./authinfo');

const pool = new Pool({
    host: '/var/run/postgresql',
    user: USERNAME,
    password: PASSWORD,
    database: 'networkmonitor'
});

module.exports = { pool };
