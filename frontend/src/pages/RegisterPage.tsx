import NavBar from "../components/Navbar";
import Register from "../components/Register";
import "../styles/App.css";

const RegisterPage = () => {
  return (
    <>
      <nav>
        <NavBar />
      </nav>
      <div className="container">
        <Register />
      </div>
    </>
  );
};

export default RegisterPage;
