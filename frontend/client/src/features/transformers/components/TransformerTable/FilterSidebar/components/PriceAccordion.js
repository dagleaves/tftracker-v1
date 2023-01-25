import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Slider from '@mui/material/Slider';
import MuiInput from '@mui/material/Input';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Switch from '@mui/material/Switch';
import Stack from '@mui/material/Stack';
import { Accordion, AccordionSummary, AccordionDetails } from './BaseAccordion';

import { useDispatch, useSelector } from 'react-redux';
import {
    search,
    updatePriceFilter,
} from '@/features/transformers';

export const FutureReleasesAccordion = () => {

    const dispatch = useDispatch();
    const { filters, availableFilters } = useSelector(state => state.search);

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


const Input = styled(MuiInput)`
  width: 42px;
`;

const minDistance = 0;

const InputSlider = () => {

    const dispatch = useDispatch();
    const { filters, availableFilters } = useSelector(state => state.search);
    const currentPriceRange = filters.price;
    const maxPriceRange = availableFilters.price;

    const handleSliderChange = (event, newValue) => {
        if (!Array.isArray(newValue)) {
            return;
          }
      
          if (newValue[1] - newValue[0] < minDistance) {
            if (activeThumb === 0) {
              const clamped = Math.min(newValue[0], 100 - minDistance);
              dispatch(updatePriceFilter([clamped, clamped + minDistance]));
            } else {
              const clamped = Math.max(newValue[1], minDistance);
              dispatch(updatePriceFilter([clamped - minDistance, clamped]));
            }
          } else {
            dispatch(updatePriceFilter(newValue));
          }
          dispatch(search());
    };

    const handleInputChange = (event) => {
        setValue(event.target.value === '' ? '' : Number(event.target.value));
    };

    const handleBlur = () => {
        if (value < 0) {
        setValue(0);
        } else if (value > 100) {
        setValue(100);
        }
    };

    return (
        <Box sx={{ width: 250 }}>
          <Typography id="input-slider" gutterBottom>
            Price
          </Typography>
          <Grid container spacing={2} alignItems="center">
            <Grid item>
                <Input
                    id='min'
                    value={currentPriceRange[0]}
                    size="small"
                    onChange={handleInputChange}
                    onBlur={handleBlur}
                    inputProps={{
                    step: 1,
                    min: maxPriceRange[0],
                    max: maxPriceRange[1],
                    type: 'number',
                    'aria-labelledby': 'input-slider',
                    }}
                />
            </Grid>
            <Grid item xs>
              <Slider
                value={currentPriceRange}
                onChange={handleSliderChange}
                aria-labelledby="input-slider"
              />
            </Grid>
            <Grid item>
              <Input
                id='max'
                value={currentPriceRange[1]}
                size="small"
                onChange={handleInputChange}
                onBlur={handleBlur}
                inputProps={{
                  step: 1,
                  min: maxPriceRange[0],
                  max: maxPriceRange[1],
                  type: 'number',
                  'aria-labelledby': 'input-slider',
                }}
              />
            </Grid>
          </Grid>
        </Box>
  );
}