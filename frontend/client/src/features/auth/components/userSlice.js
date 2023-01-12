import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import axios from '@/api/axios';


const getCSRFToken = async () => {
    try {
        await axios.get('/api/users/get-csrf/');
    } catch (err) {
        // console.log('csrf error');
    }
};

export const register = createAsyncThunk(
    'users/register',
    async (body, thunkAPI) => {
        // const body = JSON.stringify({
        //     first_name,
        //     last_name,
        //     email,
        //     password
        // });

        try {
            const res = await axios.post('/api/users/register/', body);
      
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

        try {
            const res = await axios.post('/api/users/login/', body);
      
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
              return thunkAPI.rejectWithValue(err.response.data);
          }
    }
);

export const logout = createAsyncThunk(
    'users/logout',
    async (_, thunkAPI) => {

        try {
            const res = await axios.post('/api/users/logout/');
      
            const data = res.data;

            if (res.status === 200) {
                return data;
            }
            else {
                return thunkAPI.rejectWithValue(data);
            }
          } 
          catch (err) {
              console.log(err.response.data);
              return thunkAPI.rejectWithValue(err.response.data);
          }
    }
);


export const checkAuth = createAsyncThunk(
    'users/checkAuth',
    async (_, thunkAPI) => {
        try {
            const res = await axios.get('/api/users/check-auth/');
      
            const data = res.data;

            if (res.status === 200) {
                const { dispatch } = thunkAPI;
                dispatch(getUser());

                return data;
            }
            else {
                getCSRFToken();
                return thunkAPI.rejectWithValue(data);
            }
          } 
          catch (err) {
                getCSRFToken();
                return thunkAPI.rejectWithValue(err.response.data);
          }
    }
);


export const getUser = createAsyncThunk(
    'users/me',
    async (_, thunkAPI) => {

        try {
            const res = await axios.get('/api/users/me/');
      
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
    loading: true,
    registered: false,
    errors: null,
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
                state.errors = null;
            })
            .addCase(register.fulfilled, state => {
                state.registered = true;
                state.loading = false;
                state.errors = null;
            })
            .addCase(register.rejected, (state, action) => {
                state.loading = false;
                state.errors = action.payload;
            })
            .addCase(login.pending, state => {
                state.loading = true;
                state.errors = null;
            })
            .addCase(login.fulfilled, state => {
                state.loading = false;
                state.isAuthenticated = true;
                state.errors = null;
            })
            .addCase(login.rejected, (state, action) => {
                state.loading = false;
                state.errors = action.payload;
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
                state.errors = null;
            })
            .addCase(logout.fulfilled, state => {
                state.loading = false;
                state.isAuthenticated = false;
                state.user = null;
                state.errors = null;
            })
            .addCase(logout.rejected, state => {
                state.loading = false;
            })
            .addCase(checkAuth.pending, state => {
                state.loading = true;
            })
            .addCase(checkAuth.fulfilled, state => {
                state.loading = false;
                state.isAuthenticated = true;
            })
            .addCase(checkAuth.rejected, state => {
                state.loading = false;
            })
    }
})

export const { resetRegistered } = userSlice.actions;
export const userReducer = userSlice.reducer;