import React from 'react';
import { NavBar } from "./components/NavBar"
import { Footer } from "./components/Footer"
import CssBaseline from '@mui/material/CssBaseline';

import { Outlet } from 'react-router-dom';

export const MainLayout = (props) => {
    return (
        <React.Fragment>
            <CssBaseline />
            <NavBar {...props} />
                <Outlet />
            <Footer />
        </React.Fragment>
    )
}