/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import "./style.css";

export const SideBar = ({ className }) => {
  return (
    <div className={`side-bar ${className}`}>
      <img className="savnactransparent" alt="Savnactransparent" src="/img/savnac1transparent-1.png" />
      <img className="calendar" alt="Calendar" src="/img/calendar-7.png" />
      <img className="letter" alt="Letter" src="/img/letter.png" />
      <img className="home" alt="Home" src="/img/home.png" />
      <img className="logout" alt="Logout" src="/img/logout.png" />
      <img className="literature" alt="Literature" src="/img/literature.png" />
      <img className="male-user" alt="Male user" src="/img/male-user.png" />
    </div>
  );
};
