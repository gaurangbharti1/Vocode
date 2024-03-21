import React from "react";
import { CourseNavBar } from "../../components/CourseNavBar";
import { SideBar } from "../../components/SideBar";
import { WeeklyModule } from "../../components/WeeklyModule";
import "./style.css";

export const StudentCourse = () => {
  return (
    <div className="student-course">
      <div className="div-6">
        <SideBar className="side-bar-4" />
        <CourseNavBar className="course-nav-bar-3" to="/student-resources" to1="/student-grades" to2="/student-home" />
        <WeeklyModule className="weekly-module-instance" text="WEEK 2" />
        <WeeklyModule className="weekly-module-2" text="WEEK 3" />
        <div className="overlap-10">
          <div className="rectangle-4" />
          <div className="announcements">ANNOUNCEMENTS</div>
        </div>
      </div>
    </div>
  );
};
