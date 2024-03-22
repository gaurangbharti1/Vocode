/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const CourseNavBar = ({ className, to, to1, to2, to3 }) => {
  return (
    <div className={`course-nav-bar ${className}`}>
      <div className="overlap-group">
        <div className="rectangle" />
        <div className="div" />
        <div className="course">COURSE</div>
        <Link className="resources" to={to}>
          RESOURCES
        </Link>
        <Link className="grades" to={to1}>
          GRADES
        </Link>
        <Link className="assignments" to={to2}>
          ASSIGNMENTS
        </Link>
        <Link className="text-wrapper" to={to3}>
          HOME
        </Link>
      </div>
    </div>
  );
};

CourseNavBar.propTypes = {
  to: PropTypes.string,
  to1: PropTypes.string,
  to2: PropTypes.string,
  to3: PropTypes.string,
};
