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
    const { filters, page } = useSelector(state => state.search);
    const availableFilters = page.available_filters;

    const handleToylineChange = (event) => {
        const toylines = [...filters.toyline]
        const toyline = event.target.id;
        if (!event.target.checked) {
            toylines.push(toyline);
        } else {
            const ix = toylines.indexOf(toyline);
            if (ix > -1) {
                toylines.splice(ix, 1);
            }
        }
        dispatch(updateToylineFilter(toylines));
        dispatch(search());
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
                {[...availableFilters.toyline, ...filters.toyline].map((toyline) => {
                    var name;
                    var amount;
                    if (Array.isArray(toyline)) {
                        name = toyline[0];
                        amount = toyline[1];
                    }
                    else {
                        availableFilters.toyline.forEach(toyline_list => {
                            if (toyline_list[0] === toyline) {
                                return null;
                            }
                        })
                        name = toyline;
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
                                checked={!filters.toyline.includes(name)}
                                onChange={handleToylineChange}
                            />
                        </Stack>
                    );
                })}
            </AccordionDetails>
        </Accordion>
    )
}