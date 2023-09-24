import { useRouteError } from "react-router-dom";
import Logo from "../components/Logo";

const ErrorPage = () => {
  const error = useRouteError();
  console.error(error);

  return (
    <div className="container">
      <Logo />
      <div id="error-page">
        <h1>Oh NOOOO!, You've lost the ball</h1>
        <p>Sorry, an unexpected error has occurred.</p>
      </div>
    </div>
  );
};
export default ErrorPage;
