import React from "react";
import { Breadcrumb } from "react-bootstrap";
import { Link } from "react-router-dom";

function Breadcrumbs({ links }) {
  return (
    <Breadcrumb>
      {links.map((link, index) => (
        <Breadcrumb.Item
          key={index}
          linkAs={Link}
          linkProps={{ to: link.to }}
          active={index === links.length - 1}
        >
          {link.label}
        </Breadcrumb.Item>
      ))}
    </Breadcrumb>
  );
}

export default Breadcrumbs;