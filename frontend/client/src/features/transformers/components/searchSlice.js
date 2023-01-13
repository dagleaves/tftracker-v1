import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import axios from '@/api/axios';


export const search = createAsyncThunk(
    'search/search',
    async (_, thunkAPI) => {

        const { getState } = thunkAPI;
        const { filters } = getState();
        try {
            const res = await axios.post('/api/transformers/search/', filters);
      
            const data = res.data;
            console.log(data);

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
    loading: false,
    filters: {
        'search': '',
        'toyline': '',
        'subline': '',
        'size_class': '',
        'manufacturer': '',
        'release_date': '',
        'future_releases': '',
        'price': ''
    },
    results: null,
    errors: null,
}

const searchSlice = createSlice({
    name: 'search',
    initialState,
    reducers: {
        updateSearchFilters: (state, action) => {
            state.filters = action.payload;
        }
    },
    extraReducers: builder => {
        builder
            .addCase(search.pending, state => {
                state.loading = true;
                state.errors = null;
            })
            .addCase(search.fulfilled, (state, action) => {
                state.results = action.payload;
                state.loading = false;
                state.errors = null;
            })
            .addCase(search.rejected, (state, action) => {
                state.loading = false;
                state.errors = action.payload;
            })
    }
});

export const { updateSearchFilters } = searchSlice.actions;
export const searchReducer = searchSlice.reducer;