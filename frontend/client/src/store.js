import { configureStore } from "@reduxjs/toolkit"
import { userReducer } from '@/features/auth';
import { searchReducer } from "@/features/transformers";

export const store = configureStore({
    reducer: {
        user: userReducer,
        search: searchReducer,
    },
    devTools: process.env.NODE_ENV !== 'production',
});