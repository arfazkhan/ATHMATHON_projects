import React from "react";
import Wave from "../../Components/lottie/wave-anime.json";
import Lottie from "lottie-react";
import happy from "../../Components/lottie/happy.json";

export const Addemotion = () => {
  return (
    <div className="w-full min-h-screen bg-gradient-to-t from-cyan-200 to-slate-50 relative flex justify-center items-center ">
      <div className="flex flex-wrap z-10">
        <div className="flex bg-white justify-center items-center w-64 h-64 flex-col ">
          <Lottie animationData={happy} className="w-2/3" />
          <h1 className="font-bold text-xl">Happy</h1>
        </div>
      </div>
      <Lottie animationData={Wave} className=" absolute bottom-0 w-full " />
    </div>
  );
};
