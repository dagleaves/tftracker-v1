import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import { styled } from '@mui/material/styles';
import { Link } from 'react-router-dom';


const StyledListItemButton = styled((props) => (
    <ListItemButton 
        {...props}
    />
))(({ theme }) => ({
    backgroundColor: theme.palette.action.selected,
    borderRadius: 10
}));


export const CollectionsItem = ({username, collection}) => {
    /**
     * @param username requested collection owner's username
     * @param collection collection to link to
     */

    return (
        <StyledListItemButton
            sx={{ my: 1 }}
            component={Link}
            to={`/u/${username}/collection/${collection.id}`}
        >
            <ListItemText
                primary={collection.name}
                secondary={(collection.public ? "Public" : "Private") + " - " + collection.length + " items"}
            />
            <IconButton>
                <DeleteIcon />
            </IconButton>
        </StyledListItemButton>
    )
}