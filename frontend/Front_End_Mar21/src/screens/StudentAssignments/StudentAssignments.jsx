import React from "react";
import { AssignmentCard } from "../../components/AssignmentCard";
import { CourseNavBar } from "../../components/CourseNavBar";
import { PastAssignmentCard } from "../../components/PastAssignmentCard";
import { SideBar } from "../../components/SideBar";
import "./style.css";

export const StudentAssignments = () => {
  return (
    <div className="student-assignments">
      <div className="div-3">
        <SideBar className="side-bar-instance" />
        <CourseNavBar
          className="course-nav-bar-instance"
          to="/student-resources"
          to1="/student-grades"
          to2="/student-assignments"
          to3="/student-home"
        />
        <div className="overlap-wrapper">
          <div className="upcoming-assignments-wrapper">
            <div className="upcoming-assignments">UPCOMING ASSIGNMENTS</div>
          </div>
        </div>
        <div className="past-assignments">
          <div className="past-assignments-wrapper">
            <div className="past-assignments-2">PAST ASSIGNMENTS</div>
          </div>
        </div>
        <AssignmentCard className="assignment-card-instance" />
        <PastAssignmentCard
          className="past-assignment-card-instance"
          pastAssignmentCardClassName="design-component-instance-node"
        />
        <PastAssignmentCard
          className="past-assignment-card-2"
          pastAssignmentCardClassName="design-component-instance-node"
        />
        <PastAssignmentCard
          className="past-assignment-card-3"
          pastAssignmentCardClassName="design-component-instance-node"
        />
        <PastAssignmentCard
          className="past-assignment-card-4"
          pastAssignmentCardClassName="design-component-instance-node"
        />
        <AssignmentCard
          className="assignment-card-4"
          divClassName="assignment-card-2"
          lineClassName="assignment-card-3"
        />
        <AssignmentCard
          className="assignment-card-5"
          divClassName="assignment-card-2"
          lineClassName="assignment-card-3"
        />
        <AssignmentCard
          className="assignment-card-6"
          divClassName="assignment-card-2"
          lineClassName="assignment-card-3"
        />
      </div>
    </div>
  );
};
