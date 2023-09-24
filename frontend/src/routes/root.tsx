import { useEffect, useState } from "react";
import { RootService } from "../client";
import Logo from "../components/Logo";

const Root = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Get the message from the API
    RootService.rootGetRoot().then((response) => {
      setMessage(response.message);
    });
  }, []);

  return (
    <>
      <div>
        <h1>{message ?? "Loading..."}</h1>
      </div>
      <div>
        <a href="/Home">
          <Logo />
        </a>
      </div>
    </>
  );
};

export default Root;
