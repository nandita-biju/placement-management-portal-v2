import axios from "axios";
import api from "../api/axios";

const API = "http://127.0.0.1:5000/admin";

const authHeader = () => ({
    headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
    }
});

export const getDashboard = async () => {
    const response = await axios.get(
        `${API}/dashboard`,
        authHeader()
    );

    return response.data;
};




export const getCompanies = async () => {
    const response = await api.get("/admin/companies");
    return response.data;
};

export const approveCompany = async (companyId) => {
    const response = await api.patch(`/admin/company/${companyId}/approve`);
    return response.data;
};

export const rejectCompany = async (companyId) => {
    const response = await api.patch(`/admin/company/${companyId}/reject`);
    return response.data;
};

export const deactivateCompany = async (companyId) => {
    const response = await api.put(`/admin/company/${companyId}/deactivate`);
    return response.data;
};

export const activateCompany = async (companyId) => {
    const response = await api.put(`/admin/company/${companyId}/activate`);
    return response.data;
};

export const blacklistCompany = async (companyId) => {
    const response = await api.put(`/admin/company/${companyId}/blacklist`);
    return response.data;
};

export const unblacklistCompany = async (companyId) => {
    const response = await api.put(`/admin/company/${companyId}/unblacklist`);
    return response.data;
};

export const getStudents = async () => {
    const response = await api.get("/admin/students");
    return response.data;
};

export const deactivateStudent = async (studentId) => {
    const response = await api.put(`/admin/student/${studentId}/deactivate`);
    return response.data;
};

export const activateStudent = async (studentId) => {
    const response = await api.put(`/admin/student/${studentId}/activate`);
    return response.data;
};

export const getDrives = async () => {
    const response = await api.get("/admin/drives");
    return response.data;
};

export const approveDrive = async (jobId) => {
    const response = await api.put(`/admin/approve-drive/${jobId}`);
    return response.data;
};

export const rejectDrive = async (jobId) => {
    const response = await api.put(`/admin/reject-drive/${jobId}`);
    return response.data;
};

export const searchStudents = async (query) => {

    const response = await api.get(
        `/admin/students/search?query=${query}`
    );

    return response.data;

};

export const searchCompanies = async (query) => {

    const response = await api.get(
        `/admin/companies/search?query=${query}`
    );

    return response.data;

};

export const getApplications = async () => {

    const response = await api.get("/admin/applications");

    return response.data;

};