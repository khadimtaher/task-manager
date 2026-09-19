import apiClient from "./client";

export const signupUser = async (data) => {
  const response = await apiClient.post("/signup/", data);

  return response.data;
};

export const loginUser = async (data)=>{
    const response = await apiClient.post("/login/", data)
    return response.data
};

export const getCurrentUser = async ()=>{
    const response = await apiClient.get("/me/");
    return response.data;
}

export const logoutUser = async ()=> {
    const response = await apiClient.post("/logout/");
   return response.data;
}

