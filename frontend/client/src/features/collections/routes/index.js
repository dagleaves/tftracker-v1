import axios from '@/api/axios';
import { NotFound } from "@/features/misc";

import { store } from '@/store';

import { CollectionList } from '../components/CollectionsList';
// import { CollectionDetailPage } from '../components/CollectionsDetailPage';
import { CollectionDetailPage } from '../components/CollectionDetailPage';


const getCollection = async (user, collectionid) => {
    var url = '/api/collections';
    const username = store.getState().user.user.username;
    url = url + (user === username) ? `/api/collections/me/${collectionid}/` : `api/collections/public/${collectionid}/`;
    try {
        const res = await axios.get(url);
  
        const data = res.data;
        if (res.status === 200) {
            return [user, data];
        }
        else {
            throw new Error('Not found.')
        }
      } 
      catch (err) {
        // TODO: Should probably replace with a meaningful error display
        throw new Error('Not found.')
      }
};

const getCollectionsList = async (user) => {
    const username = store.getState().user.user.username;
    const url = (user === username) ? `api/collections/me/` : 'api/collections/user/' + user + '/';
    try {
        const res = await axios.get(url);
  
        const data = res.data;

        if (res.status === 200) {
            data['username'] = user;
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
};


export const collectionsRoutes = [
    {
        path: "u/:user/collection/:collectionid",
        element: <CollectionDetailPage />,
        errorElement: <NotFound />,
        loader: ({ params }) => {
            return getCollection(params.user, params.collectionid);
        }
    },
    {
        path: "u/:user/collections",
        element: <CollectionList />,
        errorElement: <NotFound />,
        loader: ({ params }) => {
            return getCollectionsList(params.user);
        }
    },
];