import * as React from 'react';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Switch from '@mui/material/Switch';
import Stack from '@mui/material/Stack';
import { Accordion, AccordionSummary, AccordionDetails } from './BaseAccordion';

import { useDispatch, useSelector } from 'react-redux';
import {
    search,
    updateToylineFilter,
} from '@/features/transformers';

export const ToylineAccordion = () => {
    const dispatch = useDispatch();
    const { filters, availableFilters } = useSelector(state => state.search);

    const handleToylineChange = (event) => {
        const toylines = [...filters.toyline]
        const toyline = event.target.id;
        if (event.target.checked) {
            toylines.push(toyline);
        } else {
            const ix = toylines.indexOf(toyline);
            if (ix > -1) {
                toylines.splice(ix, 1);
            }
        }
        dispatch(updateToylineFilter(toylines));
    }

    return (
        <Accordion>
            <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel2a-content"
            id="panel2a-header"
            >
                <Typography>Toyline</Typography>
            </AccordionSummary>
            <AccordionDetails>
                {[...availableFilters.toyline].map((toyline) => {
                    return (
                        <Stack
                            direction='row'
                            justifyContent='space-between'
                            alignItems='center'
                            key={toyline}
                        >
                            <Stack
                                direction='row'
                                alignItems='center'
                                spacing={1}
                            >
                                <Typography>{toyline}</Typography>
                            </Stack>
                            <Switch 
                                id={toyline}
                                checked={filters.toyline.includes(toyline)}
                                onChange={handleToylineChange}
                            />
                        </Stack>
                    );
                })}
            </AccordionDetails>
        </Accordion>
    )
}