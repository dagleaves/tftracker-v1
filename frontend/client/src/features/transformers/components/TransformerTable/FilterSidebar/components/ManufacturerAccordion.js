import * as React from 'react';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Switch from '@mui/material/Switch';
import Stack from '@mui/material/Stack';
import { Accordion, AccordionSummary, AccordionDetails } from './BaseAccordion';

import { useDispatch, useSelector } from 'react-redux';
import {
    search,
    updateManufacturerFilter,
} from '@/features/transformers';

export const ManufacturerAccordion = () => {
    const dispatch = useDispatch();
    const { filters, availableFilters } = useSelector(state => state.search);

    const handleManufacturerChange = (event) => {
        const manufacturers = [...filters.manufacturer]
        const manufacturer = event.target.id;
        if (event.target.checked) {
            manufacturers.push(manufacturer);
        } else {
            const ix = manufacturers.indexOf(manufacturer);
            if (ix > -1) {
                manufacturers.splice(ix, 1);
            }
        }
        dispatch(updateManufacturerFilter(manufacturers));
        dispatch(search());
    }

    return (
        <Accordion>
            <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel2a-content"
            id="panel2a-header"
            >
                <Typography>Manufacturer</Typography>
            </AccordionSummary>
            <AccordionDetails>
                {[...availableFilters.manufacturer].map((manufacturer) => {
                    return (
                        <Stack
                            direction='row'
                            justifyContent='space-between'
                            alignItems='center'
                            key={manufacturer}
                        >
                            <Stack
                                direction='row'
                                alignItems='center'
                                spacing={1}
                            >
                                <Typography>{manufacturer}</Typography>
                            </Stack>
                            <Switch 
                                id={manufacturer}
                                checked={filters.manufacturer.includes(manufacturer)}
                                onChange={handleManufacturerChange}
                            />
                        </Stack>
                    );
                })}
            </AccordionDetails>
        </Accordion>
    )
}