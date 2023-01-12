import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { Box } from '@mui/system';
import { useLoaderData } from 'react-router';
import { Button } from '@mui/material';
import { Link } from 'react-router-dom';
import { Typography } from '@mui/material';


export const TransformerTable = () => {
    const pageData = useLoaderData();
    const count = pageData['count'];
    const responseTime = pageData['response-time'];
    const rows = pageData['results'];
    // const prevURL = pageData['previous'];
    // const nextURL = pageData['next'];

    return (
        <Box mx='auto'>
            <Typography fontSize={15} sx={{ my: 1 }}>About {count} results ({responseTime} seconds)</Typography>
            <TableContainer component={Paper}>
            <Table sx={{ minWidth: 300 }} aria-label="simple table">
                <TableHead>
                <TableRow>
                    <TableCell align='center'>Name</TableCell>
                    <TableCell align="center">Toyline</TableCell>
                    <TableCell align="center">Subline</TableCell>
                    <TableCell align="center">Size Class</TableCell>
                    <TableCell align="center">Release Date</TableCell>
                    <TableCell align="center">Price</TableCell>
                    <TableCell align="center">Manufacturer</TableCell>
                    <TableCell align="center">Details</TableCell>
                </TableRow>
                </TableHead>
                <TableBody>
                {rows.map((row) => (
                    <TableRow
                    key={row.name}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                    >
                    <TableCell component="th" scope="row" align='center'>
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
                ))}
                </TableBody>
            </Table>
            </TableContainer>
        </Box>
    );
}