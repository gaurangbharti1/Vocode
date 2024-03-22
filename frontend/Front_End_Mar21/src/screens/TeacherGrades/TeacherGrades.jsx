import React from "react";
import { AssignmentCard } from "../../components/AssignmentCard";
import { CourseNavBar } from "../../components/CourseNavBar";
import { PastAssignmentCard } from "../../components/PastAssignmentCard";
import { SideBar } from "../../components/SideBar";
import "./style.css";

export const TeacherGrades = () => {
  return (
    <div className="teacher-grades">
      <div className="div-11">
        <SideBar className="side-bar-8" />
        <CourseNavBar
          className="course-nav-bar-7"
          to="/teacher-resources"
          to2="/teacher-assignments"
          to3="/teacher-home"
        />
        <div className="assignments-3">
          <div className="ungraded-assignments-wrapper">
            <div className="ungraded-assignments">UNGRADED ASSIGNMENTS</div>
          </div>
        </div>
        <div className="past-assignments-6">
          <div className="overlap-15">
            <div className="graded-assignments-2">GRADED ASSIGNMENTS</div>
          </div>
        </div>
        <div className="assignment-card-18">
          <div className="overlap-16">
            <div className="assignment-4">ASSIGNMENT</div>
            <div className="due-date-4">Click To Grade</div>
            <div className="text-wrapper-16">Description</div>
            <img className="line-6" alt="Line" src="/img/line-6-2.svg" />
          </div>
        </div>
        <PastAssignmentCard
          className="past-assignment-card-14"
          pastAssignmentCardClassName="past-assignment-card-15"
          text="Average Grade"
        />
        <PastAssignmentCard
          className="past-assignment-card-16"
          pastAssignmentCardClassName="past-assignment-card-15"
          text="Average Grade"
        />
        <PastAssignmentCard
          className="past-assignment-card-17"
          pastAssignmentCardClassName="past-assignment-card-15"
          text="Average Grade"
        />
        <PastAssignmentCard
          className="past-assignment-card-18"
          pastAssignmentCardClassName="past-assignment-card-15"
          text="Average Grade"
        />
        <div className="assignment-card-wrapper">
          <div className="assignment-card-19">
            <div className="overlap-group-6">
              <div className="assignment-4">ASSIGNMENT</div>
              <div className="due-date-5">Click To Grade</div>
              <div className="text-wrapper-16">Description</div>
              <img className="line-7" alt="Line" src="/img/line-6-7.svg" />
            </div>
          </div>
        </div>
        <div className="assignment-card-20">
          <div className="overlap-17">
            <div className="assignment-4">ASSIGNMENT</div>
            <div className="due-date-5">Click To Grade</div>
            <div className="text-wrapper-16">Description</div>
            <img className="line-7" alt="Line" src="/img/line-6-7.svg" />
          </div>
        </div>
        <AssignmentCard
          className="assignment-card-21"
          divClassName="assignment-card-22"
          lineClassName="assignment-card-23"
          text="Click To Grade"
        />
      </div>
    </div>
  );
};
