import api from "../api/axios";

export const getProfile = async () => {
    const response = await api.get("/student/profile", {
        headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
        }
    });

    return response.data;
};