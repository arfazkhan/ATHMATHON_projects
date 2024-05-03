import React, { useEffect, useState } from "react";
import { Button, Card, Input, Typography } from "@material-tailwind/react";

import { GetReq, PatchReq } from "../../HelperFunction/PostFunction";
import { useNavigate, useParams } from "react-router-dom";
import ChartComponent from "../ChartComponent";

function ProfilePage() {
  const image = localStorage.getItem("image");
  const [updateProfile, setUpdateProfile] = useState(false);
  const [githubUrl, setGithubUrl] = useState("https://");
  const [user, setUser] = useState({});
  const [githubPorfile, setGithubProfile] = useState(null);
  const [trigger, settrigger] = useState(true);
  const [loading, setLoading] = useState(true);
  const { id } = useParams();
  const navigate = useNavigate();
  const [emo, setemo] = useState([]);
  const handleUpdateFunction = async () => {
    if (!githubUrl) return;
    const response = await PatchReq("profile/", { github: githubUrl });
    console.log(response);
    settrigger(!trigger);
  };
  useEffect(() => {
    const getEmo = async () => {
      const data = await GetReq("emotion/");
      console.log(data);
      setemo(data);
    };
    (async () => {
      let response;
      if (id) {
        response = await GetReq(`profile/?id=${id}`);
      } else {
        response = await GetReq("profile/?my=1");
      }
      setUser(response);
      setLoading(false);
    })();
    getEmo();
  }, [trigger]);

  if (loading) return <>loading</>;
  // console.log(user.github.split("/").pop());
  return (
    <>
      <div className=" min-h-screen w-full pb-9">
        <div className="flex justify-center mt-5">
          <div className="w-fit border-[8px] border-blue-400 rounded-full">
            <img src={image} alt="profile" className="w-[100px] rounded-full" />
          </div>
        </div>
        <p className="text-xl font-medium text-center mt-2">{user.username}</p>
        <div className="bg-white w-[500px] lg:w-[800px] mx-auto mt-10 rounded-xl">
          <Card color="white" className="p-5 z-10">
            <div className="mb-5">
              <Typography className="font-semibold text-lg">
                Username
              </Typography>
              <p>{user.username}</p>
            </div>
            <div className="mb-5">
              <Typography className="font-semibold text-lg">
                Total Points
              </Typography>
              <p>{user.points}</p>
            </div>
            {!id && <ChartComponent data={emo} />}
            <div className="mb-5">
              <Typography className="font-semibold text-lg">Github</Typography>
              {updateProfile ? (
                <input
                  type="text"
                  value={githubUrl}
                  onChange={(e) => setGithubUrl(e.target.value)}
                  className="bg-[#ecececbb] px-3 py-1 rounded-lg text-sm w-full"
                />
              ) : (
                <input
                  type="text"
                  disabled
                  value={
                    user.github
                      ? user.github
                      : "You have not provide your github link"
                  }
                  className="bg-[#ecececbb] px-3 py-1 rounded-lg text-sm w-full"
                />
              )}
            </div>
            {!id ? (
              <div className="flex justify-center">
                {updateProfile ? (
                  <button
                    className="px-10 py-2 rounded-lg bg-blue-500 text-white font-medium"
                    onClick={handleUpdateFunction}
                  >
                    SUBMIT
                  </button>
                ) : (
                  <button
                    className="px-10 py-2 rounded-lg bg-blue-500 text-white font-medium"
                    onClick={() => setUpdateProfile(true)}
                  >
                    UPDATE
                  </button>
                )}
              </div>
            ) : (
              <></>
            )}
            {user.github && (
              <div className="flex justify-start mt-8">
                <img
                  src={`https://github-readme-stats.vercel.app/api?username=${user.github
                    .split("/")
                    .pop()}&show_icons=true&locale=en`}
                  alt="profile"
                />
              </div>
            )}
            <div className="flex mt-3 ">
              {!id ? (
                <Button
                  variant="gradient"
                  color="red"
                  onClick={() => {
                    localStorage.clear();
                    navigate("/");
                  }}
                >
                  Log out
                </Button>
              ) : (
                <></>
              )}
            </div>
          </Card>
        </div>
      </div>
    </>
  );
}

export default ProfilePage;
