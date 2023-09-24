import React from "react";
import Validation from "../components/Validation"; // Make sure the path to Validation.tsx is correct

const ValidationPage: React.FC = () => {
  return (
    <div>
      <h1>Email Validation Page</h1>
      <Validation />
    </div>
  );
};

export default ValidationPage;
