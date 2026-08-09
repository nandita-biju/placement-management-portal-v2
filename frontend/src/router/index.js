import { createRouter, createWebHistory } from "vue-router";

// Layouts
import StudentLayout from "../layouts/StudentLayout.vue";
import CompanyLayout from "../layouts/CompanyLayout.vue";
import AdminLayout from "../layouts/AdminLayout.vue";

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
import EditCompanyProfile from "../views/Company/EditCompanyProfile.vue";
import CreateCompanyProfile from "../views/Company/CreateCompanyProfile.vue";
import CompanyStudentProfile from "../views/Company/CompanyStudentProfile.vue";


// Admin
import AdminDashboard from "../views/Admin/AdminDashboard.vue";
import ManageCompanies from "../views/Admin/ManageCompanies.vue";
import ManageStudents from "../views/Admin/ManageStudents.vue";
import ManageDrives from "../views/Admin/ManageDrives.vue";
import ManageApplications from "../views/Admin/ManageApplications.vue";

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
        path: "/company",
        component: CompanyLayout,
        children: [

            {
                path: "dashboard",
                component: CompanyDashboard
            },

            {
                path: "profile",
                component: CompanyProfile
            },

            {
                path: "profile/create",
                component: CreateCompanyProfile
            },

            {
                path: "profile/edit",
                component: EditCompanyProfile
            },

            {
                path: "create-drive",
                component: CreateDrive
            },

            {
                path: "drives",
                component: MyDrives
            },

            {
                path: "applicants/:jobId",
                component: ViewApplicants
            },

            {
                path: "student/:studentId/:jobId",
                component: CompanyStudentProfile
            },

        ]
    },
    {
        path: "/admin",
        component: AdminLayout,
        children: [

            {
                path: "dashboard",
                component: AdminDashboard
            },

            {
                path: "companies",
                component: ManageCompanies
            },

            {
                path: "students",
                component: ManageStudents
            },

            {
                path: "drives",
                component: ManageDrives
            },

            {
                path: "applications",
                component: ManageApplications
            },

            {
                path: "/admin/reports",
                component: () => import("../views/admin/AdminReports.vue")
            }

        ]
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;