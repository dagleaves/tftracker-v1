import * as React from 'react';
import PropTypes from 'prop-types';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import FilterListIcon from '@mui/icons-material/FilterList';
import { visuallyHidden } from '@mui/utils';
import SearchBar from "material-ui-search-bar";

import { useLoaderData, Link } from 'react-router-dom';
import { Button } from '@mui/material';
import { getTransformerPage } from '../hooks/getTransformerPage';


const headCells = [
  {
    id: 'name',
    numeric: false,
    label: 'Name',
  },
  {
    id: 'toyline',
    numeric: false,
    label: 'Toyline',
  },
  {
    id: 'subline',
    numeric: false,
    label: 'Subline',
  },
  {
    id: 'size_class',
    numeric: false,
    label: 'Size Class',
  },
  {
    id: 'release_date',
    numeric: false,
    label: 'Release Date',
  },
  {
    id: 'price',
    numeric: false,
    label: 'Price',
  },
  {
    id: 'manufacturer',
    numeric: false,
    label: 'Manufacturer',
  },
  {
    id: 'details',
    numeric: false,
    label: 'Details',
  },
];

const EnhancedTableHead = (props) => {
  const {order, orderBy, onRequestSort } =
    props;
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align='center'
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : 'asc'}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
};

EnhancedTableHead.propTypes = {
  onRequestSort: PropTypes.func.isRequired,
  order: PropTypes.oneOf(['asc', 'desc']).isRequired,
  orderBy: PropTypes.string.isRequired,
};

const EnhancedTableToolbar = React.forwardRef((props, filters) => {

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

        <SearchBar 
          value={filters.value.current.search}
          onChange={(newValue) => {filters.value.current.search = newValue}}
          
        />
        <Tooltip title="Filter list">
          <IconButton>
            <FilterListIcon />
          </IconButton>
        </Tooltip>
    </Toolbar>
  );
});

export const DataTable = () => {
  const pageData = useLoaderData();
  const count = pageData['count'];
  const responseTime = pageData['response-time'];
  const initRows = pageData['results'];
  const initPrevURL = pageData['previous'];
  const initNextURL = pageData['next'];


  const filters = React.useRef({
    'search': '',
    'toyline': '',
    'subline': '',
    'size_class': '',
    'manufacturer': '',
    'release_date': '',
    'future_releases': '',
    'price': ''
  });

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