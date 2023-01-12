import axios from 'axios';
import { API_SERVER } from '@/settings';

const instance = axios.create({
    baseURL: API_SERVER
});

instance.defaults.xsrfHeaderName = "X-CSRFTOKEN";
instance.defaults.xsrfCookieName = "csrftoken";
instance.defaults.headers = { 'Content-Type': 'application/json'};
instance.defaults.withCredentials = true;

// Setup response time calculation
instance.interceptors.request.use(function (config) {
    config.metadata = { startTime: new Date()}
    return config;
}, function (error) {
    return Promise.reject(error);
}); 

instance.interceptors.response.use(function (response) {
    response.config.metadata.endTime = new Date()
    response.duration = ((response.config.metadata.endTime - response.config.metadata.startTime) / 1000).toFixed(2);
    return response;
}, function (error) {
    error.config.metadata.endTime = new Date();
    error.duration = error.config.metadata.endTime - error.config.metadata.startTime;
    return Promise.reject(error);
});

export default instance;