/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const PastAssignmentCard = ({ className, text = "Description", line = "/img/line-6-1.svg" }) => {
  return (
    <div className={`past-assignment-card ${className}`}>
      <div className="div-2">
        <div className="assignment-2">ASSIGNMENT</div>
        <div className="description">{text}</div>
        <img className="img" alt="Line" src={line} />
      </div>
    </div>
  );
};

PastAssignmentCard.propTypes = {
  text: PropTypes.string,
  line: PropTypes.string,
};
