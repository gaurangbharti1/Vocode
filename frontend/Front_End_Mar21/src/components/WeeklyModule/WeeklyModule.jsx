/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const WeeklyModule = ({ className, text = "WEEK 1" }) => {
  return (
    <div className={`weekly-module ${className}`}>
      <div className="overlap-group-3">
        <div className="rectangle-2" />
        <div className="rectangle-3" />
        <div className="week">{text}</div>
        <div className="resource-assignment">
          Resource
          <br />
          assignment
          <br />
          instructions
        </div>
      </div>
    </div>
  );
};

WeeklyModule.propTypes = {
  text: PropTypes.string,
};
