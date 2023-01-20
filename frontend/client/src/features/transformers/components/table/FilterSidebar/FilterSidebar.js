import * as React from 'react';
import Paper from '@mui/material/Paper';

import { FutureReleasesAccordion } from './FutureReleasesAccordion';
import { ToylineAccordion } from './ToylineAccordion';
import { SublineAccordion } from './SublineSidebar';


export const FilterSidebar = () => {
    

    return (
        <Paper sx={{ mt: 13 }}>
            <FutureReleasesAccordion />
            <ToylineAccordion />
            <SublineAccordion />
        </Paper>
    );
}