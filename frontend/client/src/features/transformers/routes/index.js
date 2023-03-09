import { TransformerDetailPage } from "../components/TransformerDetailPage";
import axios from '@/api/axios';
import { NotFound } from "@/features/misc";

import { TransformerTable } from "../components/TransformerTable";
import { SearchProvider } from "../components/SearchProvider";

const getTransformer = async (slug) => {
    const id = slug.split('-')[0];
    try {
        const res = await axios.get(`/api/transformers/${id}`);
  
        const data = res.data;

        if (res.status === 200) {
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

const getTransformerList = async () => {
    try {
        const res = await axios.get('/api/transformers/');
  
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
};


export const transformerRoutes = [
    {
        path: "transformer/:slug",
        element: <TransformerDetailPage />,
        errorElement: <NotFound />,
        loader: ({ params }) => {
            return getTransformer(params.slug);
        }
    },
    {
        path: "transformers/",
        element: <TransformerTable />,
        errorElement: <NotFound />,
        loader: () => {
            return getTransformerList();
        }
    },
    {
        path: "search/",
        element: <SearchProvider ><TransformerTable /></SearchProvider>,
        errorElement: <NotFound />
    }
];