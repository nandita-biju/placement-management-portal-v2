import api from "../api/axios";

export const getAllDrives = async () => {

    const response = await api.get(
        "/student/drives",
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};

export const applyDrive = async (jobId) => {

    const response = await api.post(
        `/applications/apply/${jobId}`,
        {},
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};