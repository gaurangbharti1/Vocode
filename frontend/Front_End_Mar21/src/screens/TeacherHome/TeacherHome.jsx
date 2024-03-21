import React from "react";
import { TeacherSideBar } from "../../components/TeacherSideBar";
import "./style.css";

export const TeacherHome = () => {
  return (
    <div className="teacher-home">
      <div className="div-7">
        <div className="dashboard-2">DASHBOARD</div>
        <img className="course-card-7" alt="Course card" src="/img/course-card-5.svg" />
        <img className="course-card-8" alt="Course card" src="/img/course-card-6.svg" />
        <img className="course-card-9" alt="Course card" src="/img/course-card-7.svg" />
        <img className="course-card-10" alt="Course card" src="/img/course-card-8.svg" />
        <img className="course-card-11" alt="Course card" src="/img/course-card-9.svg" />
        <img className="course-card-12" alt="Course card" src="/img/course-card-10.svg" />
        <TeacherSideBar className="teacher-side-bar-instance" />
      </div>
    </div>
  );
};
