import React from "react";
import { AssignmentCard } from "../../components/AssignmentCard";
import { CourseNavBar } from "../../components/CourseNavBar";
import { PastAssignmentCard } from "../../components/PastAssignmentCard";
import { SideBar } from "../../components/SideBar";
import "./style.css";

export const TeacherAssignments = () => {
  return (
    <div className="teacher-assignments">
      <div className="div-10">
        <SideBar className="side-bar-7" />
        <CourseNavBar className="course-nav-bar-6" to="/teacher-resources" to1="/teacher-grades" to3="/teacher-home" />
        <div className="assignments-2">
          <div className="UPCOMING-assignments-wrapper">
            <div className="UPCOMING-assignments">UPCOMING ASSIGNMENTS</div>
          </div>
        </div>
        <div className="past-assignments-4">
          <div className="overlap-13">
            <div className="past-assignments-5">PAST ASSIGNMENTS</div>
          </div>
        </div>
        <AssignmentCard className="assignment-card-13" text="Due Date" />
        <PastAssignmentCard
          className="past-assignment-card-10"
          pastAssignmentCardClassName="past-assignment-card-11"
          text="Average Grade:"
        />
        <PastAssignmentCard
          className="past-assignment-card-12"
          pastAssignmentCardClassName="past-assignment-card-11"
          text="Average Grade:"
        />
        <PastAssignmentCard
          className="past-assignment-card-13"
          pastAssignmentCardClassName="past-assignment-card-11"
          text="Average Grade:"
        />
        <AssignmentCard
          className="assignment-card-14"
          divClassName="assignment-card-15"
          lineClassName="assignment-card-16"
          text="Due Date"
        />
        <AssignmentCard
          className="assignment-card-17"
          divClassName="assignment-card-15"
          lineClassName="assignment-card-16"
          text="Due Date"
        />
        <div className="overlap-14">
          <img className="vector" alt="Vector" src="/img/vector.svg" />
          <img className="frame-2" alt="Frame" src="/img/frame-4.svg" />
        </div>
      </div>
    </div>
  );
};
