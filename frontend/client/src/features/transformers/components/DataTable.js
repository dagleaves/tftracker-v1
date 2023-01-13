import * as React from 'react';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';

import { Link } from 'react-router-dom';
import { Button } from '@mui/material';
import { getTransformerPage } from '../hooks/getTransformerPage';

import { useSelector, useDispatch } from 'react-redux';
import { updateSearchFilters, search } from './searchSlice';

import { EnhancedTableHead } from './table/TableHeader';
import { EnhancedTableToolbar } from './table/TableToolbar';


export const DataTable = () => {
  const dispatch = useDispatch();

  const { filters, loading, results } = useSelector(state => state.search);

  React.useEffect(() => {
    console.log('calling dispatch')
    dispatch(search())
  });

  const pageData = results;
  const count = pageData['count'];
  const responseTime = pageData['response-time'];
  const initRows = pageData['results'];
  const initPrevURL = pageData['previous'];
  const initNextURL = pageData['next'];


  const [order, setOrder] = React.useState('asc');
  const [orderBy, setOrderBy] = React.useState('name');
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);
  const [rows, setRows] = React.useState(initRows);
  const [prevURL, setPrevURL] = React.useState(initPrevURL);
  const [nextURL, setNextURL] = React.useState(initNextURL);


  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleChangePage = (event, newPage) => {
    if (newPage > page) {
      getTransformerPage(nextURL).then(data => {
        setRows(data['results']);
        setPrevURL(data['previous']);
        setNextURL(data['next']);
      });
    } else {
      getTransformerPage(prevURL).then(data => {
        setRows(data['results']);
        setPrevURL(data['previous']);
        setNextURL(data['next']);
      });
    }
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  // Avoid a layout jump when reaching the last page with empty rows.
  const emptyRows =
    page > 0 ? Math.max(0, rowsPerPage - rows.length + 1) : 0;

  return (
    <Box mx='auto'>
      <Typography fontSize={15} sx={{ my: 1 }}>About {count} results ({responseTime} seconds)</Typography>
      <Paper sx={{ width: '100%', mb: 2 }}>
        <EnhancedTableToolbar filters={filters} />
        <TableContainer>
          <Table
            // sx={{ minWidth: 500 }}
            aria-labelledby="tableTitle"
            size={'medium'}
          >
            <EnhancedTableHead
              order={order}
              orderBy={orderBy}
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
                    height: (53) * emptyRows,
                  }}
                >
                  <TableCell colSpan={6} />
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
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
    </Box>
  );
}