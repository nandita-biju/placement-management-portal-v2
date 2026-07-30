import api from "../api/axios";

export const createProfile = async (profile) => {

    const response = await api.post(
        "/student/profile",
        profile,
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};

export const getProfile = async () => {
    const response = await api.get("/student/profile", {
        headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
        }
    });

    return response.data;
};

export const updateProfile = async (profile) => {

    const response = await api.put(
        "/student/profile",
        profile,
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};