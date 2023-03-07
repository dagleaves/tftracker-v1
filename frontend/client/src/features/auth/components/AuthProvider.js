import React from 'react';
import { useDispatch } from 'react-redux';
import { checkAuth } from '@/features/auth';

export const AuthProvider = ({ children }) => {
    const dispatch = useDispatch();
    dispatch(checkAuth());

    return (
        <React.Fragment>
            {children}
        </React.Fragment>
    );
};