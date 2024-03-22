import React from "react";
import { Link } from "react-router-dom";
import { SideBar } from "../../components/SideBar";
import "./style.css";

export const TeacherHome = () => {
  return (
    <div className="teacher-home">
      <div className="div-8">
        <div className="dashboard-2">DASHBOARD</div>
        <Link to="/teacher-course">
          <img className="course-card-7" alt="Course card" src="/img/course-card-5.svg" />
        </Link>
        <Link to="/teacher-course">
          <img className="course-card-8" alt="Course card" src="/img/course-card-6.svg" />
        </Link>
        <Link to="/teacher-course">
          <img className="course-card-9" alt="Course card" src="/img/course-card-7.svg" />
        </Link>
        <Link to="/teacher-course">
          <img className="course-card-10" alt="Course card" src="/img/course-card-8.svg" />
        </Link>
        <Link to="/teacher-course">
          <img className="course-card-11" alt="Course card" src="/img/course-card-9.svg" />
        </Link>
        <Link to="/teacher-course">
          <img className="course-card-12" alt="Course card" src="/img/course-card-10.svg" />
        </Link>
        <div className="teacher-side-bar">
          <div className="overlap-group-5">
            <SideBar className="teacher-side-bar-2" />
            <img className="add-to-clipboard" alt="Add to clipboard" src="/img/add-to-clipboard.png" />
          </div>
        </div>
      </div>
    </div>
  );
};
