import React from "react";
import { Spinner as BootstrapSpinner } from "react-bootstrap";

function Spinner() {
  return (
    <div className="d-flex justify-content-center my-5">
      <BootstrapSpinner animation="border" role="status" />
      <span className="ms-2">Loading...</span>
    </div>
  );
}

export default Spinner;