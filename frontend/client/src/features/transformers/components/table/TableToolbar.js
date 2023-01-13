import * as React from 'react';
import { alpha } from '@mui/material/styles';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import FilterListIcon from '@mui/icons-material/FilterList';
import SearchBar from "@mkyy/mui-search-bar";


export const EnhancedTableToolbar = React.forwardRef((props, filters) => {

  const handleRequestSearch = async () => {

  }

  return (
    <Toolbar
      sx={{
        pl: { sm: 2 },
        pr: { xs: 1, sm: 1 },
        ...({
          bgcolor: (theme) =>
            alpha(theme.palette.primary.main, theme.palette.action.activatedOpacity),
        }),
      }}
    >
        <Typography
          sx={{ flex: '1 1 100%' }}
          variant="h6"
          id="tableTitle"
          component="div"
        >
          Search
        </Typography>

        {/* {filters !== null ? 
        <SearchBar 
          value={filters.value.current.search}
          onChange={newValue => console.log(newValue)}
          onSearch={() => console.log('search')}
        /> : null} */}
        
        <Tooltip title="Filter list">
          <IconButton>
            <FilterListIcon />
          </IconButton>
        </Tooltip>
    </Toolbar>
  );
});
