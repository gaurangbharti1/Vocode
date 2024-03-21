/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const AssignmentCard = ({
  className,
  divClassName,
  text = "Due Date",
  lineClassName,
  line = "/img/line-6.svg",
}) => {
  return (
    <div className={`assignment-card ${className}`}>
      <div className="assignment">ASSIGNMENT</div>
      <div className={`due-date ${divClassName}`}>{text}</div>
      <div className="text-wrapper-2">Description</div>
      <img className={`line ${lineClassName}`} alt="Line" src={line} />
    </div>
  );
};

AssignmentCard.propTypes = {
  text: PropTypes.string,
  line: PropTypes.string,
};
