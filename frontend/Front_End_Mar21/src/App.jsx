import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { StudentHome } from "./screens/StudentHome";
import { StudentAssignments } from "./screens/StudentAssignments";
import { StudentCourse } from "./screens/StudentCourse";
import { StudentGrades } from "./screens/StudentGrades";
import { StudentResources } from "./screens/StudentResources";
import { TeacherHome } from "./screens/TeacherHome";
import { TeacherCourse } from "./screens/TeacherCourse";
import { TeacherAssignments } from "./screens/TeacherAssignments";
import { TeacherGrades } from "./screens/TeacherGrades";
import { TeacherResources } from "./screens/TeacherResources";

const router = createBrowserRouter([
  {
    path: "/*",
    element: <StudentHome />,
  },
  {
    path: "/student-home",
    element: <StudentHome />,
  },
  {
    path: "/student-assignments",
    element: <StudentAssignments />,
  },
  {
    path: "/student-course",
    element: <StudentCourse />,
  },
  {
    path: "/student-grades",
    element: <StudentGrades />,
  },
  {
    path: "/student-resources",
    element: <StudentResources />,
  },
  {
    path: "/teacher-home",
    element: <TeacherHome />,
  },
  {
    path: "/teacher-course",
    element: <TeacherCourse />,
  },
  {
    path: "/teacher-assignments",
    element: <TeacherAssignments />,
  },
  {
    path: "/teacher-grades",
    element: <TeacherGrades />,
  },
  {
    path: "/teacher-resources",
    element: <TeacherResources />,
  },
]);

export const App = () => {
  return <RouterProvider router={router} />;
};
