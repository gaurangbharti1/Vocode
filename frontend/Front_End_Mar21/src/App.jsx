import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { StudentHome } from "./screens/StudentHome";
import { StudentGrades } from "./screens/StudentGrades";
import { StudentResources } from "./screens/StudentResources";
import { StudentCourse } from "./screens/StudentCourse";
import { TeacherHome } from "./screens/TeacherHome";

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
    path: "/student-grades",
    element: <StudentGrades />,
  },
  {
    path: "/student-resources",
    element: <StudentResources />,
  },
  {
    path: "/student-course",
    element: <StudentCourse />,
  },
  {
    path: "/teacher-home",
    element: <TeacherHome />,
  },
]);

export const App = () => {
  return <RouterProvider router={router} />;
};
