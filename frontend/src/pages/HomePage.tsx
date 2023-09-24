import Moto from "../components/Moto";
import NavBar from "../components/Navbar";
import Logo from "../components/Logo";
import RegisterButton from "../components/RegisterButton";

const HomePage = () => {
  return (
    <>
      <nav>
        <NavBar />
      </nav>
      <div className="container">
        <div>
          <Logo />
        </div>
        <div>
          <Moto />
        </div>
        <div>
          <RegisterButton />
        </div>
        <div>
          <p>
            <p>Have an account already?</p>
            <a href="/Login">
              <p>Login</p>
            </a>
          </p>
        </div>
      </div>
    </>
  );
};

export default HomePage;
