import React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import CircleRoundedIcon from '@mui/icons-material/CircleRounded';
import { useLoaderData } from 'react-router-dom';
import { Box } from '@mui/system';


export const TransformerDetailPage = () => {
    const transformer = useLoaderData();
    var displayName;
    if (transformer['subline'] === 'None') {
        displayName = transformer['toyline'];
    } else {
        displayName = transformer['subline'];
    }
    displayName = displayName + ' ' + transformer['size_class'] + ' ' + transformer['name'];


    return (
        <div>
        <Grid container justifyContent='center' sx={{ mt: 3 }} >
            <Grid item xs={1} sx={{ mr: 8 }} >
                <Box 
                    component='img' 
                    sx={{
                        height: 200,
                        width: 200,
                    }}
                    alt='Photo of transformer' 
                    src={transformer['picture']} />
            </Grid>
            <Grid item xs={4}>
                <Typography variant="h5" sx={{ mb: 2 }} >{displayName}</Typography>
                <Typography variant="body1">{transformer['description']}</Typography>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <CircleRoundedIcon fontSize='12px' />
                        </ListItemIcon>
                        <ListItemText 
                            primaryTypographyProps={{fontSize: '14px'}} 
                            primary={`Release Date: ${transformer['release_date']}`} />
                    </ListItem>
                    <ListItem>
                        <ListItemIcon>
                            <CircleRoundedIcon fontSize='12px' />
                        </ListItemIcon>
                        <ListItemText primaryTypographyProps={{fontSize: '14px'}} primary={`Toyline: ${transformer['toyline']}`} />
                    </ListItem>
                    <ListItem>
                        <ListItemIcon>
                            <CircleRoundedIcon fontSize='12px' />
                        </ListItemIcon>
                        <ListItemText 
                            primaryTypographyProps={{fontSize: '14px'}} 
                            primary={`Subline: ${transformer['subline']}`} />
                    </ListItem>
                    <ListItem>
                        <ListItemIcon>
                            <CircleRoundedIcon fontSize='12px' />
                        </ListItemIcon>
                        <ListItemText 
                            primaryTypographyProps={{fontSize: '14px'}} 
                            primary={`Size Class: ${transformer['size_class']}`} />
                    </ListItem>
                    <ListItem>
                        <ListItemIcon>
                            <CircleRoundedIcon fontSize='12px' />
                        </ListItemIcon>
                        <ListItemText 
                            primaryTypographyProps={{fontSize: '14px'}}
                            primary={`Manufacturer: ${transformer['size_class'] === 'H' ? 'Hasbro' : 'Takara Tomy'}`} />
                    </ListItem>
                    <ListItem>
                        <ListItemIcon>
                            <CircleRoundedIcon fontSize='14px' />
                        </ListItemIcon>
                        <ListItemText 
                            primaryTypographyProps={{fontSize: '14px'}}
                            primary={`Release Price: ${transformer['price']}`} />
                    </ListItem>
                </List>
            </Grid>
        </Grid>
        </div>
    );
};
