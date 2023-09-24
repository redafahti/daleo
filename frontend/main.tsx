import React from "react";
import ReactDOM from "react-dom/client";
import "bootstrap/dist/css/bootstrap.css";
import "react-datepicker/dist/react-datepicker.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Root from "./src/routes/root";
import HomePage from "./src/pages/HomePage";
import RegisterPage from "./src/pages/RegisterPage";
import ValidationPage from "./src/pages/ValidationPage";
import LoginPage from "./src/pages/LoginPage";
import ErrorPage from "./src/pages/ErrorPage";
import { OpenAPI } from "./src/client";

OpenAPI.BASE = "http://localhost:8000";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/Home",
    element: <HomePage />,
  },
  {
    path: "/Register",
    element: <RegisterPage />,
  },
  {
    path: "/Validate",
    element: <ValidationPage />,
  },
  {
    path: "/Login",
    element: <LoginPage />,
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
