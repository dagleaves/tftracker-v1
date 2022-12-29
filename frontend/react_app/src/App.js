import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import { Provider } from 'react-redux';
import { store } from './store';

import { publicRoutes } from './routes';
import { protectedRoutes } from './routes';

import { ThemeProvider, createTheme } from '@mui/material/styles';

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

function App(props) {
  const router = createBrowserRouter([
    ...publicRoutes,
    ...protectedRoutes
  ]);

  return (
    <Provider store={store}>
      <ThemeProvider theme={darkTheme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </Provider>
  )
}

export default App;
