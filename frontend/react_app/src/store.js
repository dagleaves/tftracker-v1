import { configureStore } from "@reduxjs/toolkit"
import { userReducer } from '@/features/auth';

export const store = configureStore({
    reducer: {
        user: userReducer,
    },
    devTools: process.env.NODE_ENV !== 'production',
});