import * as React from 'react';
import Typography from '@mui/material/Typography';
import { useLoaderData } from 'react-router-dom';

export const CollectionDetailPage = () => {
    const collection = useLoaderData();

    return (
        <Typography>
            {collection.name}
        </Typography>
    );
}