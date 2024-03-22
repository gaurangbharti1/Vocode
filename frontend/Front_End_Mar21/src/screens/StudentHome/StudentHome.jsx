import React from "react";
import { Link } from "react-router-dom";
import { CourseCard } from "../../components/CourseCard";
import { SideBar } from "../../components/SideBar";
import { TaskCard } from "../../components/TaskCard";
import "./style.css";

export const StudentHome = () => {
  return (
    <div className="student-home">
      <div className="div-4">
        <div className="dashboard">DASHBOARD</div>
        <div className="upcoming-tasks">UPCOMING TASKS</div>
        <CourseCard className="course-card-instance" />
        <Link to="/student-course">
          <img className="course-card-2" alt="Course card" src="/img/course-card.svg" />
        </Link>
        <Link to="/student-course">
          <img className="course-card-3" alt="Course card" src="/img/course-card-1.svg" />
        </Link>
        <Link to="/student-course">
          <img className="course-card-4" alt="Course card" src="/img/course-card-2.svg" />
        </Link>
        <Link to="/student-course">
          <img className="course-card-5" alt="Course card" src="/img/course-card-3.svg" />
        </Link>
        <Link to="/student-course">
          <img className="course-card-6" alt="Course card" src="/img/course-card-4.svg" />
        </Link>
        <img className="line-3" alt="Line" src="/img/line-4.svg" />
        <TaskCard className="task-card-instance" />
        <TaskCard className="task-card-2" />
        <TaskCard className="task-card-3" />
        <TaskCard className="task-card-4" />
        <SideBar className="side-bar-2" />
      </div>
    </div>
  );
};
