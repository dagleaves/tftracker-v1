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
    const { filters, page } = useSelector(state => state.search);
    const availableFilters = page.available_filters;

    const handleManufacturerChange = (event) => {
        const manufacturers = [...filters.manufacturer]
        const manufacturer = event.target.id;
        if (!event.target.checked) {
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
                {[...availableFilters.manufacturer, ...filters.manufacturer].map((manufacturer) => {
                    var name;
                    var amount;
                    if (Array.isArray(manufacturer)) {
                        name = manufacturer[0];
                        amount = manufacturer[1];
                    }
                    else {
                        availableFilters.manufacturer.forEach(manufacturer_list => {
                            if (manufacturer_list[0] === manufacturer) {
                                return null;
                            }
                        })
                        name = manufacturer;
                        amount = 0;
                    }

                    return (
                        <Stack
                            direction='row'
                            justifyContent='space-between'
                            alignItems='center'
                            key={name}
                        >
                            <Stack
                                direction='row'
                                alignItems='center'
                                spacing={1}
                            >
                                <Typography>{name}</Typography>
                                <Typography sx={{ fontSize: '0.75rem' }}>({amount})</Typography>
                            </Stack>
                            <Switch 
                                id={name}
                                checked={!filters.manufacturer.includes(name)}
                                onChange={handleManufacturerChange}
                            />
                        </Stack>
                    );
                })}
            </AccordionDetails>
        </Accordion>
    )
}