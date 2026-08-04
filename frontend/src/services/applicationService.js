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


export const exportApplications = async () => {
    const response = await api.get("/applications/export", {
        responseType: "blob"
    });

    return response.data;
};