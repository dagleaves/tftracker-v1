import React from 'react';
import { ProtectedRoute } from '@/utils/ProtectedRoute';
import { transformerRoutes } from '@/features/transformers';
import { collectionsRoutes } from '@/features/collections';

import { About } from '@/features/misc';


export const protectedRoutes = [
    {
        element: <ProtectedRoute />,
        children: [
            {
                path: "about",
                element: <About />,
            },
            ...transformerRoutes,
            ...collectionsRoutes,
        ],
    },
];