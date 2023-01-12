import React from "react";
import { Outlet, Navigate } from "react-router-dom";
import { useSelector } from "react-redux";

export const ProtectedRoute = () => {
    const { loading, isAuthenticated } = useSelector(state => state.user);
    
    if (loading)
        return null;

    return isAuthenticated ? <Outlet /> : <Navigate to="/login" />
}