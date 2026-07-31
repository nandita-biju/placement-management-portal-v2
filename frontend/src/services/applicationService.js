import api from "../api/axios";

export const getMyApplications = async () => {

    const response = await api.get(
        "/applications/my-applications",
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};