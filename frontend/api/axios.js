const express = require('express');
const axios = require('axios');

const baseAxios = axios.create({
    baseURL: process.env.API_URL
});

baseAxios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
baseAxios.defaults.xsrfCookieName = "csrftoken";
baseAxios.defaults.headers = { 'Content-Type': 'application/json'};
baseAxios.defaults.withCredentials = true;

module.exports = baseAxios;