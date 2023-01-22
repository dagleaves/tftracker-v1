import * as React from 'react';
import Paper from '@mui/material/Paper';

import { FutureReleasesAccordion } from './components/FutureReleasesAccordion';
import { ToylineAccordion } from './components/ToylineAccordion';
import { SublineAccordion } from './components/SublineAccordion';
import { ManufacturerAccordion } from './components/ManufacturerAccordion';


export const FilterSidebar = () => {
    

    return (
        <Paper sx={{ mt: 13 }}>
            <FutureReleasesAccordion />
            <ToylineAccordion />
            <SublineAccordion />
            <ManufacturerAccordion />
        </Paper>
    );
}