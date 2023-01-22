import * as React from 'react';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Switch from '@mui/material/Switch';
import Stack from '@mui/material/Stack';
import { Accordion, AccordionSummary, AccordionDetails } from './BaseAccordion';

import { useDispatch, useSelector } from 'react-redux';
import {
    search,
    updateFutureReleasesFilter,
} from '@/features/transformers';

export const FutureReleasesAccordion = () => {

    const dispatch = useDispatch();
    const { filters } = useSelector(state => state.search);

    const handleFutureReleasesChange = (event) => {
        dispatch(updateFutureReleasesFilter(event.target.checked));
        dispatch(search());
    };

    return (
        <Accordion>
            <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1a-content"
            id="panel1a-header"
            >
                <Typography>Future Releases</Typography>
            </AccordionSummary>
            <AccordionDetails>
                <Stack
                    direction='row'
                    justifyContent='space-between'
                    alignItems='center'
                >
                    <Typography>
                        Include Future Releases
                    </Typography>
                    <Switch 
                        checked={filters.future_releases}
                        onChange={handleFutureReleasesChange}
                    />
                </Stack>
            </AccordionDetails>
        </Accordion>
    )
}