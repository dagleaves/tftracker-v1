import axios from '@/api/axios';

export const getTransformerPage = async (url) => {
    try {
        const res = await axios.get(url, {
            baseURL: ''
        });
  
        const data = res.data; 

        if (res.status === 200) {
            data['response-time'] = res.duration;
            return data;
        }
        else {
            throw new Error('Not found.')
        }
    } 
    catch (err) {
        // TODO: Should probably replace with a meaningful error display
        throw new Error('Not found.')
    }
}