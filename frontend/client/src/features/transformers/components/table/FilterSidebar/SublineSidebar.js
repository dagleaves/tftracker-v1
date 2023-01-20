import * as React from 'react';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Switch from '@mui/material/Switch';
import Stack from '@mui/material/Stack';
import { Accordion, AccordionSummary, AccordionDetails } from './BaseAccordion';

import { useDispatch, useSelector } from 'react-redux';
import {
    search,
    updateSublineFilter,
} from '@/features/transformers';

export const SublineAccordion = () => {
    const dispatch = useDispatch();
    const { filters, page } = useSelector(state => state.search);
    const availableFilters = page.available_filters;

    const handleSublineChange = (event) => {
        const sublines = [...filters.subline]
        const subline = event.target.id;
        if (!event.target.checked) {
            sublines.push(subline);
        } else {
            const ix = sublines.indexOf(subline);
            if (ix > -1) {
                sublines.splice(ix, 1);
            }
        }
        dispatch(updateSublineFilter(sublines));
        dispatch(search());
    }

    return (
        <Accordion>
            <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel2a-content"
            id="panel2a-header"
            >
                <Typography>Subline</Typography>
            </AccordionSummary>
            <AccordionDetails>
                {[...availableFilters.subline, ...filters.subline].map((subline) => {
                    var name;
                    var amount;
                    if (Array.isArray(subline)) {
                        name = subline[0];
                        amount = subline[1];
                    }
                    else {
                        availableFilters.subline.forEach(subline_list => {
                            if (subline_list[0] === subline) {
                                return null;
                            }
                        })
                        name = subline;
                        amount = 0;
                    }

                    return (
                        <Stack
                            direction='row'
                            justifyContent='space-between'
                            alignItems='center'
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
                                checked={!filters.subline.includes(name)}
                                onChange={handleSublineChange}
                            />
                        </Stack>
                    );
                })}
            </AccordionDetails>
        </Accordion>
    )
}