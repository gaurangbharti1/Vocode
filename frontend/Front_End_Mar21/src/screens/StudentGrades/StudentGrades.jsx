import React from "react";
import { AssignmentCard } from "../../components/AssignmentCard";
import { CourseNavBar } from "../../components/CourseNavBar";
import { PastAssignmentCard } from "../../components/PastAssignmentCard";
import { SideBar } from "../../components/SideBar";
import "./style.css";

export const StudentGrades = () => {
  return (
    <div className="student-grades">
      <div className="div-6">
        <SideBar className="side-bar-4" />
        <CourseNavBar
          className="course-nav-bar-3"
          to="/student-resources"
          to1="/student-grades"
          to2="/student-assignments"
          to3="/student-home"
        />
        <div className="overlap-group-wrapper">
          <div className="graded-assignments-wrapper">
            <div className="graded-assignments">GRADED ASSIGNMENTS</div>
          </div>
        </div>
        <div className="past-assignments-3">
          <div className="submitted-for-wrapper">
            <div className="submitted-for">SUBMITTED&nbsp;&nbsp;&nbsp;&nbsp;FOR GRADING</div>
          </div>
        </div>
        <div className="assignment-card-7">
          <div className="overlap-3">
            <div className="assignment-3">ASSIGNMENT</div>
            <div className="due-date-2">Grade:</div>
            <div className="text-wrapper-8">Description</div>
            <img className="line-4" alt="Line" src="/img/line-6-2.svg" />
          </div>
        </div>
        <PastAssignmentCard
          className="past-assignment-card-5"
          pastAssignmentCardClassName="past-assignment-card-6"
          text="Submitted On:"
        />
        <PastAssignmentCard
          className="past-assignment-card-7"
          pastAssignmentCardClassName="past-assignment-card-6"
          text="Submitted On:"
        />
        <PastAssignmentCard
          className="past-assignment-card-8"
          pastAssignmentCardClassName="past-assignment-card-6"
          text="Submitted On:"
        />
        <PastAssignmentCard
          className="past-assignment-card-9"
          pastAssignmentCardClassName="past-assignment-card-6"
          text="Submitted On:"
        />
        <div className="frame">
          <div className="assignment-card-8">
            <div className="overlap-group-4">
              <div className="assignment-3">ASSIGNMENT</div>
              <div className="due-date-3">Grade:</div>
              <div className="text-wrapper-8">Description</div>
              <img className="line-5" alt="Line" src="/img/line-6-7.svg" />
            </div>
          </div>
        </div>
        <div className="assignment-card-9">
          <div className="overlap-4">
            <div className="assignment-3">ASSIGNMENT</div>
            <div className="due-date-3">Grade:</div>
            <div className="text-wrapper-8">Description</div>
            <img className="line-5" alt="Line" src="/img/line-6-7.svg" />
          </div>
        </div>
        <AssignmentCard
          className="assignment-card-10"
          divClassName="assignment-card-11"
          lineClassName="assignment-card-12"
          text="Grade:"
        />
      </div>
    </div>
  );
};
