import React from 'react';

import { MainLayout } from '@/components/Layout';
import { authRoutes } from '@/features/auth';
import { NotFound } from '@/features/misc';
import { protectedRoutes } from './protected';
import { Home } from '@/features/misc';


export const publicRoutes = [
    {
        path: "/",
        element: <MainLayout />,
        children: [
            { index: true, element: <Home />},
            ...protectedRoutes,
            {
                path: "*",
                element: <NotFound />,
            },
        ],
    },
    ...authRoutes,
];