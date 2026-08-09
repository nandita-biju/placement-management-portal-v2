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

    const response = await api.get(
        "/student/profile",
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

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


export const getStudentById = async (studentId) => {

    const response = await api.get(
        `/student/${studentId}`,
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }
    );

    return response.data;
};


/* =========================================
   GET MY APPLICATIONS
   ========================================= */

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

export const uploadResume = async (formData) => {

    const response = await api.post(
        "/student/profile/resume",
        formData,
        {
            headers: {
                Authorization:
                    `Bearer ${localStorage.getItem("token")}`,
                "Content-Type": "multipart/form-data"
            }
        }
    );

    return response.data;
};


/* =========================================
   VIEW OWN RESUME (Student)
   ========================================= */

export const viewResume = async () => {

    const response = await api.get(
        "/student/profile/resume",
        {
            responseType: "blob"
        }
    );

    return response;
};


/* =========================================
   VIEW STUDENT RESUME (Admin/Company)
   ========================================= */

export const viewStudentResume = async (studentId) => {

    const response = await api.get(
        `/student/student/${studentId}/resume`,
        {
            responseType: "blob"
        }
    );

    return response;
};


/* =========================================
   DELETE OWN RESUME (Student)
   ========================================= */

export const deleteResume = async () => {

    const response = await api.delete(
        "/student/profile/resume"
    );

    return response.data;
};

export const getMyInterviews = async () => {

    const response = await api.get(
        "/student/interviews"
    );

    return response.data;

};

export const getStudentPlacementHistory = async (studentId) => {
  const response = await api.get(
    `/admin/student/${studentId}/placement-history`
  );

  return response.data;
};