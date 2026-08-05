import api from "../api/axios";

export const getMyApplications = async () => {
    const response = await api.get("/applications/my-applications");
    return response.data;
};

export const exportApplications = async () => {
    const response = await api.get("/applications/export");
    return response.data;
};

export const checkExportStatus = async (taskId) => {
    const response = await api.get(`/applications/export/status/${taskId}`);
    return response.data;
};