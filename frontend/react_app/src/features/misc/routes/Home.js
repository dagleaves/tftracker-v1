import React from 'react'
import CssBaseline from '@mui/material/CssBaseline';
import { Link } from 'react-router-dom';

export const Home = () => {
    return (
        <React.Fragment>
            <CssBaseline />
           
            <div>
                <h1>Home Page</h1>
                <Link to="/login">Login</Link>
            </div>

        </React.Fragment>
    )
}