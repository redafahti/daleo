import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { RegisterService } from "../client";
import { UserCreate } from "../client";

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    confirmPassword: "",
    email: "",
    mobile: "",
    firstName: "",
    lastName: "",
    userPhoto: "",
    gender: "Male", // Default gender
  });

  const [registrationSuccess, setRegistrationSuccess] = useState(false);

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Send the formData to backend API
    const userCreateData: UserCreate = {
      username: formData.username,
      password: formData.password,
      email: formData.email,
      mobile: formData.mobile,
      first_name: formData.firstName,
      last_name: formData.lastName,
      user_photo: formData.userPhoto,
      gender: formData.gender,
    };

    try {
      await RegisterService.registerNewUser(userCreateData);
      setRegistrationSuccess(true);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    if (registrationSuccess) {
      // Redirect to the validation page upon successful registration
      window.location.href = "/validate"; // Replace with your validation route
    }
  }, [registrationSuccess]);

  return (
    <div>
      <form className="row g-3" onSubmit={handleSubmit}>
        <div className="col-md-4">
          <label htmlFor="username" className="form-label">
            Username:
          </label>
          <input
            type="text"
            id="username"
            name="username"
            className="form-control"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-md-4">
          <label htmlFor="password" className="form-label">
            Password:
          </label>
          <input
            type="password"
            id="password"
            name="password"
            className="form-control"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-md-4">
          <label htmlFor="confirmPassword" className="form-label">
            Confirm Password:
          </label>
          <input
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            className="form-control"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-md-6">
          <label htmlFor="email" className="form-label">
            Email Address:
          </label>
          <input
            type="email"
            id="email"
            name="email"
            className="form-control"
            placeholder="name@example.com"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-md-6">
          <label htmlFor="mobile" className="form-label">
            Mobile Number:
          </label>
          <input
            type="text"
            id="mobile"
            name="mobile"
            className="form-control"
            placeholder="06XXXXXXXX"
            value={formData.mobile}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-md-4">
          <label htmlFor="firstName" className="form-label">
            First Name:
          </label>
          <input
            type="text"
            id="firstName"
            name="firstName"
            className="form-control"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-md-4">
          <label htmlFor="lastName" className="form-label">
            Last Name:
          </label>
          <input
            type="text"
            id="lastName"
            name="lastName"
            className="form-control"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-md-1">
          <label htmlFor="gender" className="form-label">
            Gender
          </label>
          <select
            id="gender"
            name="gender"
            className="form-select"
            value={formData.gender}
            onChange={handleChange}
            required
          >
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </div>
        <div className="d-grid gap-2">
          <button type="submit" className="btn btn-primary">
            <h1> Register </h1>
          </button>
        </div>
      </form>
      <p>
        Already have an account? <Link to="/Login">Login</Link>
      </p>
    </div>
  );
};

export default Register;
