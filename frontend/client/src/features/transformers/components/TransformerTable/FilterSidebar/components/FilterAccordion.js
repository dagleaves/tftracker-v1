import * as React from 'react';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Switch from '@mui/material/Switch';
import Stack from '@mui/material/Stack';
import { Accordion, AccordionSummary, AccordionDetails } from './BaseAccordion';

import { useDispatch, useSelector } from 'react-redux';
import {
    search,
    updateFilter
} from '@/features/transformers';

export const FilterAccordion = ({ filterKey, filterDisplayName}) => {
    const dispatch = useDispatch();
    const { filters, availableFilters } = useSelector(state => state.search);

    const handleChange = (event) => {
        const currentFilter = [...filters[filterKey]]
        const selectedFilter = event.target.id;
        if (event.target.checked) {
            currentFilter.push(selectedFilter);
        } else {
            const ix = currentFilter.indexOf(selectedFilter);
            if (ix > -1) {
                currentFilter.splice(ix, 1);
            }
        }
        dispatch(updateFilter({
            'key': filterKey,
            'value': currentFilter
        }));
        dispatch(search());
    }

    return (
        <Accordion>
            <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel2a-content"
            id="panel2a-header"
            >
                <Typography>{filterDisplayName}</Typography>
            </AccordionSummary>
            <AccordionDetails>
                {[...availableFilters[filterKey]].map((filterOption) => {
                    return (
                        <Stack
                            direction='row'
                            justifyContent='space-between'
                            alignItems='center'
                            key={filterOption}
                        >
                            <Stack
                                direction='row'
                                alignItems='center'
                                spacing={1}
                            >
                                <Typography>{filterOption}</Typography>
                            </Stack>
                            <Switch 
                                id={filterOption}
                                checked={filters[filterKey].includes(filterOption)}
                                onChange={handleChange}
                            />
                        </Stack>
                    );
                })}
            </AccordionDetails>
        </Accordion>
    )
}