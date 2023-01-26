import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Slider from '@mui/material/Slider';
import MuiInput from '@mui/material/Input';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionSummary, AccordionDetails } from './BaseAccordion';

import { useDispatch, useSelector } from 'react-redux';
import {
    updatePriceFilter,
} from '@/features/transformers';

export const PriceAccordion = () => {
    return (
        <Accordion>
            <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1a-content"
            id="panel1a-header"
            >
              <Typography>Price</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <InputSlider />
            </AccordionDetails>
        </Accordion>
    )
}


const Input = styled(MuiInput)`
  // width: 42px;
`;

const minDistance = 0;

const InputSlider = () => {

    const dispatch = useDispatch();
    const { filters, availableFilters } = useSelector(state => state.search);
    const currentPriceRange = filters.price;
    const maxPriceRange = availableFilters.price;

    const handleSliderChange = (event, newValue, activeThumb) => {
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
    };

    const handleInputChange = (event) => {
      if (event.target.value === '') {
        return;
      }
      const newValue = Number(event.target.value);
      const newRange = [...currentPriceRange];
      if (event.target.id === 'min') {
        newRange[0] = newValue;
      } else {
        newRange[1] = newValue;
      }
      dispatch(updatePriceFilter(newRange));
    };

    // TODO: NEED TO CONVERT TO STACK FOR INPUTS -- TOO WIDE CURRENTLY

    return (
        <Box sx={{ width: 250 }}>
          <Typography id="input-slider" gutterBottom>
            Price
          </Typography>
          <Grid container spacing={2} alignItems="center">
            <Grid item>
                <Input
                    id='min'
                    value={currentPriceRange.lower ? currentPriceRange[0] : maxPriceRange[0]}
                    size="small"
                    onChange={handleInputChange}
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
                value={currentPriceRange.upper ? currentPriceRange[1] : maxPriceRange[1]}
                size="small"
                onChange={handleInputChange}
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