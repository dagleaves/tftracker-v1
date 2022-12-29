import React from "react";
import { Outlet, Navigate } from "react-router-dom";
import { useSelector } from "react-redux";

export const ProtectedRoute = () => {
    const { isAuthenticated } = useSelector(state => state.user);
    return (
        isAuthenticated ? <Outlet /> : <Navigate to="/login" />
    )
}