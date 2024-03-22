import React from "react";
import { CourseNavBar } from "../../components/CourseNavBar";
import { SideBar } from "../../components/SideBar";
import "./style.css";

export const TeacherResources = () => {
  return (
    <div className="teacher-resources">
      <div className="div-12">
        <SideBar className="side-bar-9" />
        <CourseNavBar
          className="course-nav-bar-8"
          to1="/teacher-grades"
          to2="/teacher-assignments"
          to3="/teacher-course"
        />
        <div className="overlap-18">
          <div className="text-wrapper-17">Lecture 1 Slides PDF</div>
        </div>
        <div className="overlap-19">
          <div className="text-wrapper-18">Lecture 2 Notes</div>
        </div>
        <div className="overlap-20">
          <div className="text-wrapper-19">Lecture 3 Slides PDF</div>
        </div>
        <div className="overlap-21">
          <div className="rectangle-7" />
          <div className="text-wrapper-20">Chapter 1: Extra Reading</div>
        </div>
        <div className="overlap-22">
          <div className="text-wrapper-21">Lecture 2 Slides PDF</div>
        </div>
        <div className="overlap-23">
          <div className="text-wrapper-22">Lecture 1 Notes</div>
        </div>
        <div className="frame-wrapper">
          <div className="frame-3">
            <img className="frame-4" alt="Frame" src="/img/frame-5.svg" />
            <div className="text-wrapper-23">Upload New Resource</div>
          </div>
        </div>
      </div>
    </div>
  );
};
