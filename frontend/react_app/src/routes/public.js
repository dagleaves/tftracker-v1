import React from 'react';

import { MainLayout } from '@/components/Layout';
import { Home } from '@/features/misc';
import { authRoutes } from '@/features/auth';
import { NotFound } from '@/features/misc';
import { protectedRoutes } from './protected';

export const publicRoutes = [
    {
        path: "/",
        element: <MainLayout />,
        children: [
            { index: true, element: <Home /> },
            ...protectedRoutes,
            {
                path: "*",
                element: <NotFound />,
            },
            // ...authRoutes,
        ],
    },
    ...authRoutes,
];