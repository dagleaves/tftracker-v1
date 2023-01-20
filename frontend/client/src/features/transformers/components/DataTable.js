import * as React from 'react';
import Grid from "@mui/material/Grid";
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Divider from '@mui/material/Divider';
import Button from '@mui/material/Button';

import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { 
  search, 
  updatePageNumber, 
  updateRowsPerPage,
  updateOrderBy,
  updateAscending,
} from './searchSlice';

import { EnhancedTableHead } from './table/TableHeader';
import { EnhancedTableToolbar } from './table/TableToolbar';
import { FilterSidebar } from './table/FilterSidebar';


export const DataTable = () => {
  const dispatch = useDispatch();
  const { page, pagination, sorting, responseTime } = useSelector(state => state.search);
  const { order, ascending } = sorting;
  const { rowsPerPage, pageNumber } = pagination;

  const count = page['count'];
  const rows = page['results'];


  const handleRequestSort = (event, property) => {
    const isAsc = order === property && ascending === 'true';
    dispatch(updateAscending(isAsc ? 'false' : 'true'));
    dispatch(updateOrderBy(property));
    dispatch(search());
  };

  const handleChangePage = (event, newPage) => {
    dispatch(updatePageNumber(newPage));
    dispatch(search());
  };

  const handleChangeRowsPerPage = (event) => {
    dispatch(updateRowsPerPage(parseInt(event.target.value, 10)));
    dispatch(updatePageNumber(0));
    dispatch(search());
  };

  // Avoid a layout jump when reaching the last pageNumber with empty rows.
  const emptyRows =
    pageNumber < 0 ? Math.max(0, rowsPerPage - rows.length + 1) : 0;

  return (
    <Grid container justifyContent='center' spacing={2}>
      <Grid item xs={2}>
        <FilterSidebar />
      </Grid>

      <Grid item>
        <Divider orientation='vertical' sx={{mt: 13}} />
      </Grid>

      <Grid item xs={6}>
        <Box>
          <Typography fontSize={15} sx={{ my: 1 }}>Found {count} results ({responseTime} seconds)</Typography>
          <Paper sx={{ width: '100%', mb: 2 }}>
            <EnhancedTableToolbar />
            <TableContainer>
              <Table
                // sx={{ minWidth: 500 }}
                aria-labelledby="tableTitle"
                size={'medium'}
              >
                <EnhancedTableHead
                  order={ascending === 'false' ? 'asc' : 'desc'}
                  orderBy={order}
                  onRequestSort={handleRequestSort}
                />
                <TableBody>
                  {rows.map((row) => {

                      return (
                        <TableRow
                          hover
                        //   onClick={(event) => handleClick(event, row.name)}
                          tabIndex={-1}
                          key={row.name}
                        >
                          <TableCell
                            component="th"
                            // id={labelId}
                            scope="row"
                          >
                            {row.name}
                          </TableCell>
                          <TableCell align="center">{row.toyline}</TableCell>
                          <TableCell align="center">{row.subline}</TableCell>
                          <TableCell align="center">{row.size_class}</TableCell>
                          <TableCell align="center">{row.release_date}</TableCell>
                          <TableCell align="center">{row.price}</TableCell>
                          <TableCell align="center">{row.manufacturer}</TableCell>
                          <TableCell align="center">
                              <Button variant='contained' component={Link} to={'/transformers/' + row.id + '-' + row.name}>View</Button>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  {emptyRows > 0 && (
                    <TableRow
                      style={{
                        height: (52) * emptyRows,
                      }}
                    >
                      <TableCell colSpan={8} />
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
            <TablePagination
              rowsPerPageOptions={[5, 10, 25]}
              component="div"
              count={count}
              rowsPerPage={rowsPerPage}
              page={pageNumber}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
            />
          </Paper>
        </Box>
      </Grid>
    </Grid>
    
  );
}