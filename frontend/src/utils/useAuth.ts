import { useState, useEffect } from "react";
import { LoginService } from "../client";
import { UsersService } from "../client";

// A custom hook that returns the authentication status and functions
export const useAuth = () => {
  // A state variable that indicates whether the user is logged in or not
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // A function that simulates logging in the user
  const login = async (username: string, password: string) => {
    try {
      // Make a POST request to the login endpoint with the username and password
      const response = await LoginService.loginLoginForAccessToken({
        username,
        password,
      });
      // Get the access token and token type from the response data
      const access_token = response.access_token;
      // Store the access token in the local storage
      localStorage.setItem("access_token", access_token);
      // Set the state variable to true
      setIsLoggedIn(true);
    } catch (error) {
      // Handle the error
      console.error(error);
    }
  };

  // A function that simulates logging out the user
  const logout = () => {
    // Remove the access token from the local storage
    localStorage.removeItem("access_token");
    // Set the state variable to false
    setIsLoggedIn(false);
  };

  // A function that checks the authentication status of the user
  const checkAuth = async () => {
    try {
      // Get the access token from the local storage
      const access_token = localStorage.getItem("access_token");
      // If there is no access token, return false
      if (!access_token) return false;
      // Make a GET request to the me endpoint
      const response = await UsersService.usersGetMyUserProfile();
      // Get the username from the response data
      const username = response.username;
      // If there is a username, return true
      if (username) return true;
    } catch (error) {
      // Handle the error
      console.error(error);
    }
    // Otherwise, return false
    return false;
  };

  // Use an effect hook to fetch the authentication status of the user on mount and whenever the access token changes
  const access_token = localStorage.getItem("access_token");
  useEffect(() => {
    const fetchAuth = async () => {
      const data = await checkAuth();
      setIsLoggedIn(data);
    };
    fetchAuth();
  }, [access_token]);

  // Return an object with the authentication status and functions
  return { isLoggedIn, login, logout };
};


