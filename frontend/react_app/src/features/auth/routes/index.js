import { Login } from "../components/Login";
import { SignUp } from "../components/Signup";

export const authRoutes = [
    {
        path: "/login",
        element: <Login />,
    },
    {
        path: "/signup",
        element: <SignUp />,
    }
];