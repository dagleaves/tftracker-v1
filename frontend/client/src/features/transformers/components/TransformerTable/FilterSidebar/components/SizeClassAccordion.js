import * as React from 'react';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Switch from '@mui/material/Switch';
import Stack from '@mui/material/Stack';
import { Accordion, AccordionSummary, AccordionDetails } from './BaseAccordion';

import { useDispatch, useSelector } from 'react-redux';
import {
    search,
    updateSizeClassFilter,
} from '@/features/transformers';

export const SizeClassAccordion = () => {
    const dispatch = useDispatch();
    const { filters, availableFilters } = useSelector(state => state.search);

    const handleSizeClassChange = (event) => {
        const sizeClasses = [...filters.size_class]
        const sizeClass = event.target.id;
        if (event.target.checked) {
            sizeClasses.push(sizeClass);
        } else {
            const ix = sizeClasses.indexOf(sizeClass);
            if (ix > -1) {
                sizeClasses.splice(ix, 1);
            }
        }
        dispatch(updateSizeClassFilter(sizeClasses));
    }

    return (
        <Accordion>
            <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel2a-content"
            id="panel2a-header"
            >
                <Typography>Size Class</Typography>
            </AccordionSummary>
            <AccordionDetails>
                {[...availableFilters.size_class].map((sizeClass) => {
                    return (
                        <Stack
                            direction='row'
                            justifyContent='space-between'
                            alignItems='center'
                            key={sizeClass}
                        >
                            <Stack
                                direction='row'
                                alignItems='center'
                                spacing={1}
                            >
                                <Typography>{sizeClass}</Typography>
                            </Stack>
                            <Switch 
                                id={sizeClass}
                                checked={filters.size_class.includes(sizeClass)}
                                onChange={handleSizeClassChange}
                            />
                        </Stack>
                    );
                })}
            </AccordionDetails>
        </Accordion>
    )
}