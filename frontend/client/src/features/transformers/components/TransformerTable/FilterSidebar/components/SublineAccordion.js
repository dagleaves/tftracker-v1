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
    const { filters, availableFilters } = useSelector(state => state.search);
    // const { filters, page } = useSelector(state => state.search);
    // const availableFilters = page.availableFilters;

    const handleSublineChange = (event) => {
        const sublines = [...filters.subline]
        const subline = event.target.id;
        if (event.target.checked) {
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
                {[...availableFilters.subline].map((subline) => {
                    return (
                        <Stack
                            direction='row'
                            justifyContent='space-between'
                            alignItems='center'
                            key={subline}
                        >
                            <Stack
                                direction='row'
                                alignItems='center'
                                spacing={1}
                            >
                                <Typography>{subline}</Typography>
                                {/* <Typography sx={{ fontSize: '0.75rem' }}>({amount})</Typography> */}
                            </Stack>
                            <Switch 
                                id={subline}
                                checked={filters.subline.includes(subline)}
                                onChange={handleSublineChange}
                            />
                        </Stack>
                    );
                })}
            </AccordionDetails>
        </Accordion>
    )
}