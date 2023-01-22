import * as React from 'react';
import { alpha } from '@mui/material/styles';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import SearchBar from "@mkyy/mui-search-bar";

import { useSelector, useDispatch } from 'react-redux';
import { search, updateSearchFilter, resetSearchState } from '@/features/transformers';


export const EnhancedTableToolbar = () => {
  const dispatch = useDispatch();
  const { filters } = useSelector(state => state.search);

  const onChange = (newValue) => {
    dispatch(updateSearchFilter(newValue));
  }

  const handleRequestSearch = () => {
    dispatch(search());
  }

  const handleReset = () => {
    dispatch(resetSearchState());
    dispatch(search());
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
          sx={{ mr: 3 }}
          variant="h6"
          id="tableTitle"
          onClick={handleReset}
          component={Button}
        >
          Search
        </Typography>

        <SearchBar 
          value={filters.search}
          onChange={onChange}
          onSearch={handleRequestSearch}
          style={{ color: 'black' }}
        />
        
    </Toolbar>
  );
};
