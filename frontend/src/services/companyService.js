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