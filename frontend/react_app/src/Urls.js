import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import Login from "./components/Login";

function Urls(props) {

    return (
        <div>
            <BrowserRouter>
                <Routes>
                    <Route path="/login/" element={<Login {...props} />} /> 
                </Routes>
            </BrowserRouter>
        </div>
    )
};

export default Urls;