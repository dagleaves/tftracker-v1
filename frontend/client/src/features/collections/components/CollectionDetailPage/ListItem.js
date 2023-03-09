import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import Typography from '@mui/material/Typography';
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


export const CollectionItem = ({username, transformer}) => {
    /**
     * @param username requested collection owner's username
     * @param transformer transformer to show
     */

    return (
        <StyledListItemButton
            sx={{ my: 1 }}
            component={Link}
            to={`/transformer/${transformer.id}-${transformer.name}`}
        >
            <ListItemText
                primary={transformer.name}
                secondary={
                    <React.Fragment>
                      <Typography
                        sx={{ display: 'inline' }}
                        component="span"
                        variant="body2"
                        color="text.primary"
                      >
                        {transformer.toyline}: {transformer.subline} - {transformer.size_class}
                      </Typography>
                    </React.Fragment>
                  }
            />
            <IconButton>
                <DeleteIcon />
            </IconButton>
        </StyledListItemButton>
    )
}