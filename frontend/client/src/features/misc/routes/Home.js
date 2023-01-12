import React from 'react'
import CssBaseline from '@mui/material/CssBaseline';
import { Link } from 'react-router-dom';
import { Button } from '@mui/material';

export const Home = () => {
    return (
        <React.Fragment>
            <CssBaseline />
           
            <div align='center'>
                <h1>Home Page</h1>
                <Button variant='contained' component={Link} to='/signup'>Register</Button>
                <Button variant='contained' component={Link} to='/login'>Login</Button>
                <Button variant='contained' component={Link} to='/transformers/'>Transformers</Button>
                <Button variant='contained' component={Link} to='/search/'>Search</Button>
                <Button variant='contained' component={Link} to='/about'>About</Button>
            </div>

        </React.Fragment>
    )
}