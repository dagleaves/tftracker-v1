import * as React from 'react';
import { Grid } from '@mui/material';
import { useLoaderData } from 'react-router-dom';
import { CollectionItem } from './ListItem';
import { useSelector } from 'react-redux';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import List from '@mui/material/List';


export const CollectionDetailPage = () => {
    const { loading } = useSelector(state => state.user);
    const [username, collection] = useLoaderData();

    return loading ? (
        <Box sx={{ display: 'flex' }} justifyContent="center">
            <CircularProgress />
        </Box> 
    ) : (
            <Grid
                container
                direction='column'
                justifyContent='center'
                alignItems="center"
                spacing={3}
            >
                <Grid 
                    item 
                >
                    <Typography variant='h4'>
                        u/{username}'s {collection.name}
                    </Typography>
                </Grid>
                <Grid 
                    container
                    item
                    justifyContent='center' 
                    alignItems='center'
                    spacing={2}
                >
                    <List>
                        {collection.items.map((transformer) => {
                            return (
                                <CollectionItem username={username} transformer={transformer} />
                            )
                        })}
                    </List>
                </Grid>
            </Grid>
    );
}