import { useState } from "react";
import { EmailValidationService } from "../client";

// A custom hook that returns the validation status and functions
export const useValidate = () => {
  // A state variable that indicates whether the user is validated or not
  const [isValidated, setIsValidated] = useState(false);

  // A function that simulates validation in the user
  const validate = async (email: string, validationCode: string) => {
    try {
      // Make a POST request to the validation endpoint with the email and validation code
      await EmailValidationService.emailValidationValidateUserEmail(
        email,
        validationCode,
      );
      // If the request is successful, set the state variable to true
      setIsValidated(true);
    } catch (error) {
      // Handle the error
      console.error(error);
    }

  };

  // Return an object with the validation status and validation function
  return { isValidated, validate };
};
