import axios from "axios";
const accessToken = localStorage.getItem("token");
const hostUrl = "http://localhost:8000";
export const PostReq = async (url, data) => {
  try {
    const headers = {
      // "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    };
    const response = (await axios.post(`${hostUrl}/${url}`, data, { headers }))
      .data;

    return response;
  } catch (error) {
    console.log(error);
    return null;
  }
};
export const PatchReq = async (url, data) => {
  try {
    const headers = {
      // "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    };
    const response = (await axios.patch(`${hostUrl}/${url}`, data, { headers }))
      .data;

    return response;
  } catch (error) {
    console.log(error);
    return null;
  }
};
export const GetReq = async (url) => {
  try {
    const headers = {
      // "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    };
    const response = (await axios.get(`${hostUrl}/${url}`, { headers })).data;

    return response;
  } catch (error) {
    console.log(error);
    return null;
  }
};
