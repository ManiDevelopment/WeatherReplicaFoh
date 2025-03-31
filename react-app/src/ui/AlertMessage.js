import React from "react";
import { Alert } from "react-bootstrap";

function AlertMessage({ message }) {
  return (
    <Alert variant="danger" className="my-3">
      <strong>Error:</strong> {message}
    </Alert>
  );
}

export default AlertMessage;