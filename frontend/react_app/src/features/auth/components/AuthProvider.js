import React, { Fragment , useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { checkAuth } from '@/features/auth';

export const AuthProvider = ({ children }) => {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(checkAuth());
    }, [dispatch]);

    return (
        <Fragment>
            {children}
        </Fragment>
    );
};