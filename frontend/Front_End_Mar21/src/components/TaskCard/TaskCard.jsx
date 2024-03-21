/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import "./style.css";

export const TaskCard = ({ className }) => {
  return (
    <div className={`task-card ${className}`}>
      <div className="text-wrapper-5">Task</div>
      <div className="short-description">Short Description</div>
      <div className="text-wrapper-6">Course</div>
      <div className="text-wrapper-7">Due Date</div>
      <img className="line-2" alt="Line" />
    </div>
  );
};
