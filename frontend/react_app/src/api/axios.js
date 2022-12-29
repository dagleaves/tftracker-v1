import axios from 'axios';
import { API_SERVER } from '@/settings';

const instance = axios.create({
    baseURL: API_SERVER
});

instance.defaults.xsrfHeaderName = "X-CSRFTOKEN";
instance.defaults.xsrfCookieName = "csrftoken";
instance.defaults.headers = { 'Content-Type': 'application/json'};
// instance.defaults.withCredentials = true;

export default instance;