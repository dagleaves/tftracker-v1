import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import { Provider } from 'react-redux';
import { store } from './store';
import { AuthProvider } from './features/auth';

import { publicRoutes } from './routes';

import { ThemeProvider, createTheme } from '@mui/material/styles';

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

function App() {
  const router = createBrowserRouter([
    ...publicRoutes,
  ]);

  

  return (
    <Provider store={store}>
      <AuthProvider>
        <ThemeProvider theme={darkTheme}>
          <RouterProvider router={router} />
        </ThemeProvider>
      </AuthProvider>
    </Provider>
  )
}

export default App;
