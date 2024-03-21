import React from "react";
import { AssignmentCard } from "../../components/AssignmentCard";
import { CourseNavBar } from "../../components/CourseNavBar";
import { PastAssignmentCard } from "../../components/PastAssignmentCard";
import { SideBar } from "../../components/SideBar";
import "./style.css";

export const StudentGrades = () => {
  return (
    <div className="student-grades">
      <div className="div-3">
        <SideBar className="design-component-instance-node" />
        <CourseNavBar
          className="course-nav-bar-instance"
          to="/student-resources"
          to1="/student-grades"
          to2="/student-home"
        />
        <div className="overlap-wrapper">
          <div className="graded-assignments-wrapper">
            <div className="graded-assignments">GRADED ASSIGNMENTS</div>
          </div>
        </div>
        <div className="past-assignments">
          <div className="submitted-for-wrapper">
            <div className="submitted-for">SUBMITTED&nbsp;&nbsp;&nbsp;&nbsp;FOR GRADING</div>
          </div>
        </div>
        <div className="overlap-group-wrapper">
          <div className="overlap-2">
            <div className="assignment-3">ASSIGNMENT</div>
            <div className="due-date-2">Grade:</div>
            <div className="text-wrapper-8">Description</div>
            <img className="line-3" alt="Line" src="/img/line-6-2.svg" />
          </div>
        </div>
        <PastAssignmentCard className="past-assignment-card-instance" line="/img/line-6-3.svg" text="Submitted On:" />
        <PastAssignmentCard className="past-assignment-card-2" line="/img/line-6-3.svg" text="Submitted On:" />
        <PastAssignmentCard className="past-assignment-card-3" line="/img/line-6-3.svg" text="Submitted On:" />
        <PastAssignmentCard className="past-assignment-card-4" line="/img/line-6-3.svg" text="Submitted On:" />
        <div className="frame">
          <div className="assignment-card-2">
            <div className="overlap-group-5">
              <div className="assignment-3">ASSIGNMENT</div>
              <div className="due-date-3">Grade:</div>
              <div className="text-wrapper-8">Description</div>
              <img className="line-4" alt="Line" src="/img/line-6-7.svg" />
            </div>
          </div>
        </div>
        <div className="assignment-card-3">
          <div className="overlap-3">
            <div className="assignment-3">ASSIGNMENT</div>
            <div className="due-date-3">Grade:</div>
            <div className="text-wrapper-8">Description</div>
            <img className="line-4" alt="Line" src="/img/line-6-7.svg" />
          </div>
        </div>
        <AssignmentCard
          className="assignment-card-instance"
          divClassName="assignment-card-4"
          line="/img/line-6-7.svg"
          lineClassName="assignment-card-5"
          text="Grade:"
        />
      </div>
    </div>
  );
};
