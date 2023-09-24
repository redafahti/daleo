import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useValidate } from "../utils/useValidate";

const Validation: React.FC = () => {
  const [formData, setFormData] = useState({
    email: "",
    validationCode: "",
  });

  const validation = useValidate();
  const [isValidated, setIsValidated] = useState(false);
  const [validationError, setValidationError] = useState("");

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      // Call the validate function from the useValidate hook
      await validation.validate(formData.email, formData.validationCode);

      // Set the validation status
      setIsValidated(true);
      setValidationError("");
    } catch (error) {
      // Validation failed
      setIsValidated(false);
      setValidationError("Validation failed. Please check your code.");
    }
  };

  useEffect(() => {
    if (isValidated) {
      // Redirect to the login page after successful validation
      window.location.href = "/login";
    }
  }, [isValidated]);

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="row mb-3">
          <label htmlFor="email" className="col-sm-2 col-form-label">
            Email:
          </label>
          <div className="col-sm-10">
            <input
              type="email"
              className="form-control"
              id="email"
              name="email"
              placeholder="name@example.com"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        <div className="row mb-3">
          <label htmlFor="validationCode" className="col-sm-2 col-form-label">
            Validation Code:
          </label>
          <div className="col-sm-10">
            <input
              type="validationCode"
              className="form-control"
              id="validationCode"
              name="validationCode"
              value={formData.validationCode}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        <div className="d-grid gap-2">
          <button type="submit" className="btn btn-primary">
            Validate
          </button>
        </div>
      </form>
      {validationError && <p>{validationError}</p>}
      {isValidated && !validationError && (
        <p>Validation succeeded! You will be redirected to the login page.</p>
      )}
      <p>
        Don't have an account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
};

export default Validation;
