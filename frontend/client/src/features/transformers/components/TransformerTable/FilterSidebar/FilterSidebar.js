import * as React from 'react';
import Paper from '@mui/material/Paper';

import { FutureReleasesAccordion } from './components/FutureReleasesAccordion';
import { ToylineAccordion } from './components/ToylineAccordion';
import { SublineAccordion } from './components/SublineAccordion';
import { ManufacturerAccordion } from './components/ManufacturerAccordion';
import { SizeClassAccordion } from './components/SizeClassAccordion';
import { FilterAccordion } from './components/FilterAccordion';


export const FilterSidebar = () => {
    const filters = [
        ['toyline', 'Toyline'],
        ['subline', 'Subline'],
        ['manufacturer', 'Manufacturer'],
        ['size_class', 'Size Class']
    ]

    return (
        <Paper sx={{ mt: 13 }}>
            <FutureReleasesAccordion />
            {filters.map((filter) => {
                return (
                    <FilterAccordion key={filter[0]} filterKey={filter[0]} filterDisplayName={filter[1]} />
                )
            })}
        </Paper>
        
    );
}