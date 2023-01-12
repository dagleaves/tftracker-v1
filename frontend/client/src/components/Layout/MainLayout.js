import React from 'react';
import { NavBar } from "./components/NavBar"
import { Footer } from "./components/Footer"
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';

import { Outlet, useLocation } from 'react-router-dom';
import { Helmet } from 'react-helmet';

export const MainLayout = () => {
    const location = useLocation();
    var title = location.pathname.split('/').pop();
    if (title === '') {
        title = 'Home';
    } else {
        title = title.charAt(0).toUpperCase() + title.slice(1);
    }
    var content = title;
    title = 'TFTracker | ' + title;

    return (
        <>
            <Helmet>
                <title>{title}</title>
                <meta name='description' content={content} />
            </Helmet>
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    minHeight: '100vh',
                }}
            >
                <CssBaseline />
                <NavBar />
                    <Outlet />
                <Footer />
            </Box>
        </>
    )
}