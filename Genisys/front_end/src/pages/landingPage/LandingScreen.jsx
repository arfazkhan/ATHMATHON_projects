import React from "react";
import Lottie, { useLottie } from "lottie-react";
import Wave from "../../Components/lottie/wave-anime.json";
import Monkey from "../../Components/lottie/monkey.json";
import { Button, Typography } from "@material-tailwind/react";
import { Link } from "react-router-dom";

const LandingScreen = () => {
  //   const { wave_View } = useLottie(anime_Options);
  return (
    <div className="w-full min-h-screen bg-gradient-to-t from-cyan-200 to-slate-50 relative">
      <div className="absolute w-full h-screen flex items-center z-10">
        <div className="grid grid-cols-2 px-40">
          <div className="text-6xl font-black flex flex-col gap-3">
            <h1 className=" ">Experience life </h1>
            <h1 className="text-blue-400">from a refreshing perspective</h1>
            <div className="flex mt-8">
              <Link to="/login">
                <Button
                  variant="gradient"
                  color="light-blue"
                  size="lg"
                  className="text-xl rounded-2xl"
                >
                  {" "}
                  Start Life{" "}
                </Button>
              </Link>
            </div>
          </div>{" "}
          <div className=" flex justify-center">
            <Lottie animationData={Monkey} className="w-80" />
          </div>
        </div>
      </div>
      <Lottie animationData={Wave} className=" absolute bottom-0 w-full" />
    </div>
  );
};

export default LandingScreen;
