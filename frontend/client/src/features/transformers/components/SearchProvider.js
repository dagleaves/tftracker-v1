import React, { Fragment , useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { search, getAvailableFilters } from './searchSlice';

export const SearchProvider = ({ children }) => {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(search());
        dispatch(getAvailableFilters())
    });

    return (
        <Fragment>
            {children}
        </Fragment>
    );
};