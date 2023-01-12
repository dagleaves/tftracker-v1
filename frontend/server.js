const express = require('express');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(express.json());

app.use(express.static('client/build'));
app.get('/*', (req, res) => {
    return res.sendFile(path.resolve(__dirname, 'client', 'build', 'index.html'));
})

const port = process.env.PORT || 5000;
app.listen(port, () => console.log(`Listening on port ${port}`));

