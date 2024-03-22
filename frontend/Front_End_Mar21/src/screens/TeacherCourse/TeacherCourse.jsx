import React from "react";
import { CourseNavBar } from "../../components/CourseNavBar";
import { SideBar } from "../../components/SideBar";
import { WeeklyModule } from "../../components/WeeklyModule";
import "./style.css";

export const TeacherCourse = () => {
  return (
    <div className="teacher-course">
      <div className="div-9">
        <SideBar className="side-bar-6" />
        <CourseNavBar
          className="course-nav-bar-5"
          to="/teacher-resources"
          to1="/teacher-grades"
          to2="/teacher-assignments"
          to3="/teacher-home"
        />
        <WeeklyModule className="weekly-module-3" text="WEEK 2" />
        <WeeklyModule className="weekly-module-4" text="WEEK 3" />
        <div className="overlap-11">
          <div className="rectangle-5" />
          <div className="write-announcement">WRITE ANNOUNCEMENT:</div>
          <div className="announcements-2">ANNOUNCEMENTS</div>
          <div className="rectangle-6" />
        </div>
        <div className="overlap-12">
          <div className="text-wrapper-15">Write New Weekly Module</div>
        </div>
      </div>
    </div>
  );
};
