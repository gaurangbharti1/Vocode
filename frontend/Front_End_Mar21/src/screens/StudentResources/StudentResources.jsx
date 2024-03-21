import React from "react";
import { CourseNavBar } from "../../components/CourseNavBar";
import { SideBar } from "../../components/SideBar";
import "./style.css";

export const StudentResources = () => {
  return (
    <div className="student-resources">
      <div className="div-5">
        <SideBar className="side-bar-3" />
        <CourseNavBar className="course-nav-bar-2" to="/student-resources" to1="/student-grades" to2="/student-home" />
        <div className="overlap-4">
          <div className="text-wrapper-9">Lecture 1 Slides PDF</div>
        </div>
        <div className="overlap-5">
          <div className="text-wrapper-10">Lecture 2 Notes</div>
        </div>
        <div className="overlap-6">
          <div className="text-wrapper-11">Lecture 3 Slides PDF</div>
        </div>
        <div className="overlap-7">
          <div className="text-wrapper-12">Chapter 1: Extra Reading</div>
        </div>
        <div className="overlap-8">
          <div className="text-wrapper-13">Lecture 2 Slides PDF</div>
        </div>
        <div className="overlap-9">
          <div className="text-wrapper-14">Lecture 1 Notes</div>
        </div>
      </div>
    </div>
  );
};
