/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import { SideBar } from "../SideBar";
import "./style.css";

export const TeacherSideBar = ({ className }) => {
  return (
    <div className={`teacher-side-bar ${className}`}>
      <div className="overlap-group-4">
        <SideBar className="side-bar-instance" />
        <img className="add-to-clipboard" alt="Add to clipboard" />
      </div>
    </div>
  );
};
