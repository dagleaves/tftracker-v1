import { Login } from "../components/Login";
import { Register } from "../components/Register";

export const authRoutes = [
    {
        path: "/login",
        element: <Login />,
    },
    {
        path: "/register",
        element: <Register />,
    }
];