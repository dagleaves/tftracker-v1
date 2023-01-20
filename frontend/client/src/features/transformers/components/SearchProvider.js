import React, { Fragment , useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { search } from './searchSlice';

export const SearchProvider = ({ children }) => {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(search(1));
    });

    return (
        <Fragment>
            {children}
        </Fragment>
    );
};