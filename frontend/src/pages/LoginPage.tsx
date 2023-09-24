import NavBar from "../components/Navbar";
import Login from "../components/Login";

const LoginPage = () => {
  return (
    <>
      <nav>
        <NavBar />
      </nav>
      <div className="container">
        <Login />
      </div>
    </>
  );
};

export default LoginPage;
