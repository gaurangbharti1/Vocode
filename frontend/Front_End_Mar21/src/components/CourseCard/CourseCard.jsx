/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const CourseCard = ({ className }) => {
  return (
    <Link className={`course-card ${className}`} to="/student-course">
      <div className="overlap-group-2">
        <div className="overlap">
          <div className="text-wrapper-3">Course Name</div>
        </div>
        <div className="div-wrapper">
          <div className="text-wrapper-4">Course Image</div>
        </div>
      </div>
    </Link>
  );
};
