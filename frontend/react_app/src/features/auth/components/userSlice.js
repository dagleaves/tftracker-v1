import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import axios from '@/api/axios';
import Cookies from 'js-cookie';


const getCSRFToken = async () => {
    try {
        await axios.get('/api/users/get-csrf/');
    } catch (err) {
        
    }
};

export const register = createAsyncThunk(
    'users/register',
    async ({body}, thunkAPI) => {
        // const body = JSON.stringify({
        //     first_name,
        //     last_name,
        //     email,
        //     password
        // });

        await getCSRFToken();
        try {
            const res = await axios.post('/api/users/register/', body, {
              headers: { 'Content-Type': 'application/json'}
            });
      
            const data = res.data;

            if (res.status === 201) {
                return data;
            }
            else {
                return thunkAPI.rejectWithValue(data);
            }
          } 
          catch (err) {
              return thunkAPI.rejectWithValue(err.response.data);
          }
    }
);

export const login = createAsyncThunk(
    'users/login',
    async (body, thunkAPI) => {
        // const body = JSON.stringify({
        //     email,
        //     password
        // });

        await getCSRFToken();
        try {
            const res = await axios.post('/api/users/login/', body, {
                // withCredentials: true
            });
      
            const data = res.data;

            if (res.status === 200) {
                const { dispatch } = thunkAPI;
                dispatch(getUser());

                return data;
            }
            else {
                return thunkAPI.rejectWithValue(data);
            }
          } 
          catch (err) {
              console.log(err);
              return thunkAPI.rejectWithValue(err.response.data);
          }
    }
);

export const logout = createAsyncThunk(
    'users/logout',
    async (_, thunkAPI) => {

        await getCSRFToken();
        try {
            const res = await axios.post('/api/users/logout/', {
                withCredentials: true
            });
      
            const data = res.data;

            if (res.status === 200) {
                return data;
            }
            else {
                return thunkAPI.rejectWithValue(data);
            }
          } 
          catch (err) {
              console.log(err);
              return thunkAPI.rejectWithValue(err.response.data);
          }
    }
);

const getUser = createAsyncThunk(
    'users/me',
    async (_, thunkAPI) => {

        // await getCSRFToken();
        try {
            const res = await axios.get('/api/users/me/', {
                withCredentials: true
            })
      
            const data = res.data;

            if (res.status === 200) {
                return data;
            }
            else {
                return thunkAPI.rejectWithValue(data);
            }
          } 
          catch (err) {
              return thunkAPI.rejectWithValue(err.response.data);
          }
    }
);

const initialState = {
    isAuthenticated: false,
    user: null,
    loading: false,
    registered: false,
}

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        resetRegistered: (state) => {
            state.registered = false;
        }

    },
    extraReducers: builder => {
        builder
            .addCase(register.pending, state => {
                state.loading = true;
            })
            .addCase(register.fulfilled, state => {
                state.registered = true;
                state.loading = false;
            })
            .addCase(register.rejected, state => {
                // TODO: add error message state
                state.loading = false;
            })
            .addCase(login.pending, state => {
                state.loading = true;
            })
            .addCase(login.fulfilled, state => {
                state.loading = false;
                state.isAuthenticated = true;
            })
            .addCase(login.rejected, state => {
                state.loading = false;
            })
            .addCase(getUser.pending, state => {
                state.loading = true;
            })
            .addCase(getUser.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload;
            })
            .addCase(getUser.rejected, state => {
                state.loading = false;
            })
            .addCase(logout.pending, state => {
                state.loading = true;
            })
            .addCase(logout.fulfilled, state => {
                state.loading = false;
                state.isAuthenticated = false;
                state.user = null;
            })
            .addCase(logout.rejected, state => {
                state.loading = false;
            })
    }
})

export const { resetRegistered } = userSlice.actions;
export const userReducer = userSlice.reducer;