import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../utils/useAuth";

const Login: React.FC = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const auth = useAuth();
  const [isLoggedOut, setIsLoggedOut] = useState(false);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Here, you can implement your login logic
    // For example, call the login function from the useAuth hook
    auth.login(formData.email, formData.password);

    // Set the isLoggedOut state to true for redirection
    setIsLoggedOut(true);
  };

  useEffect(() => {
    if (isLoggedOut) {
      // Redirect the user to a different page after successful login
      window.location.href = "/";
    }
  }, [isLoggedOut]);

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
          <label htmlFor="password" className="col-sm-2 col-form-label">
            Password:
          </label>
          <div className="col-sm-10">
            <input
              type="password"
              className="form-control"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        <div className="d-grid gap-2">
          <button type="submit" className="btn btn-primary">
            <h1> Login </h1>
          </button>
        </div>
      </form>
      <p>
        Don't have an account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
};

export default Login;
