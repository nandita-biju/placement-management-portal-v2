import api from "../api/axios";

export const getCompanyProfile = async () => {

    const response = await api.get(
        "/company/profile",
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};

export const createCompanyProfile = async (profile) => {

    const response = await api.post(
        "/company/profile",
        profile,
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};

export const updateCompanyProfile = async (profile) => {

    const response = await api.put(
        "/company/profile",
        profile,
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};

export const getMyDrives = async () => {

    const response = await api.get(
        "/jobs/my-jobs",
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};

export const getApplicants = async (jobId) => {

    const response = await api.get(
        `/jobs/${jobId}/applications`,
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};

export const updateApplicationStatus = async (applicationId, status) => {

    const response = await api.patch(
        `/applications/${applicationId}/status`,
        { status },
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};