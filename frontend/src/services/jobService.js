import api from "../api/axios";

const authHeader = () => ({
    headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
    }
});

export const createJob = async (job) => {

    const response = await api.post(
        "/jobs/create",
        job,
        authHeader()
    );

    return response.data;
};

export const getMyJobs = async () => {

    const response = await api.get(
        "/jobs/my-jobs",
        authHeader()
    );

    return response.data;
};

export const getApplicants = async (jobId) => {

    const response = await api.get(
        `/jobs/${jobId}/applications`,
        authHeader()
    );

    return response.data;
};