const express = require('express');

const router = express.Router();
const axios = require('../../api/axios');

router.post('/api/users/register/', async (req, res) => {
    try {
        const register_res = await axios.post('/api/users/register', req.body);
        const data = await register_res.jsos();
        return res.status(register_res.status).json(data);
    } catch(err) {
        console.log(err);
        return res.status(500).json({
            error: 'Something went wrong during registration'
        })
    }
});

module.exports = router;