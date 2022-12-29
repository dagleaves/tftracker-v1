import React from 'react';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';

export const Footer = () => {
    return (
      <Typography variant="body2" color="text.secondary" align="center">
        {'Copyright © '}
        <Link color="inherit" href="">
          TFTracker.com
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
    );
  }