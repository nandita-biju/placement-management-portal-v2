import { createRouter, createWebHistory } from "vue-router";

// Layouts
import StudentLayout from "../layouts/StudentLayout.vue";

// Auth
import LoginView from "../views/Auth/LoginView.vue";
import RegisterStudentView from "../views/Auth/RegisterStudentView.vue";
import RegisterCompanyView from "../views/Auth/RegisterCompanyView.vue";

// Student
import StudentDashboard from "../views/Student/StudentDashboard.vue";
import StudentProfile from "../views/Student/StudentProfile.vue";
import CreateStudentProfile from "../views/Student/CreateStudentProfile.vue";
import EditStudentProfile from "../views/Student/EditStudentProfile.vue";
import BrowseDrives from "../views/Student/BrowseDrives.vue";
import MyApplications from "../views/Student/MyApplications.vue";

// Company
import CompanyDashboard from "../views/Company/CompanyDashboard.vue";
import CompanyProfile from "../views/Company/CompanyProfile.vue";
import CreateDrive from "../views/Company/CreateDrive.vue";
import MyDrives from "../views/Company/MyDrives.vue";
import ViewApplicants from "../views/Company/ViewApplicants.vue";

// Admin
import AdminDashboard from "../views/Admin/AdminDashboard.vue";
import ManageCompanies from "../views/Admin/ManageCompanies.vue";
import ManageStudents from "../views/Admin/ManageStudents.vue";
import ManageDrives from "../views/Admin/ManageDrives.vue";

const routes = [
    {
        path: "/",
        component: LoginView
    },

    {
        path: "/register/student",
        component: RegisterStudentView
    },

    {
        path: "/register/company",
        component: RegisterCompanyView
    },

    {
        path: "/student",
        component: StudentLayout,

        children: [

            {
                path: "dashboard",
                component: StudentDashboard
            },

            {
                path: "profile",
                component: StudentProfile
            },

            {
                path: "profile/edit",
                component: EditStudentProfile
            },

            {
                path: "drives",
                component: BrowseDrives
            },

            {
                path: "applications",
                component: MyApplications
            }

        ]
    },

    {
        path: "/student/profile/create",
        component: CreateStudentProfile
    },

    {
        path: "/company/dashboard",
        component: CompanyDashboard
    },

    {
        path: "/company/profile",
        component: CompanyProfile
    },

    {
        path: "/company/create-drive",
        component: CreateDrive
    },

    {
        path: "/company/drives",
        component: MyDrives
    },

    {
        path: "/company/applicants",
        component: ViewApplicants
    },

    {
        path: "/admin/dashboard",
        component: AdminDashboard
    },

    {
        path: "/admin/companies",
        component: ManageCompanies
    },

    {
        path: "/admin/students",
        component: ManageStudents
    },

    {
        path: "/admin/drives",
        component: ManageDrives
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;