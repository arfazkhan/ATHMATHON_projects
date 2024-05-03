import React from "react";
import Wave from "../../Components/lottie/wave-anime.json";
import reward from "../../Components/lottie/reward.json";
import Lottie from "lottie-react";
import { Button, Textarea } from "@material-tailwind/react";
import { Link } from "react-router-dom";

const Addreward = ({ submitTask, Setstate, task }) => {
  return (
    <div className="flex  bg-white rounded-lg px-9 py-6 z-10 gap-5 ">
      <div className="">
        <Lottie animationData={reward} className="w-72" />
      </div>
      <div className="">
        <h1 className="text-3xl font-bold">Add a reward!</h1>
        <div className=" h-full mt-5">
          <Textarea
            label="Add your reward"
            onChange={(e) => {
              Setstate((prev) => ({ ...prev, reward: e.target.value }));
            }}
          ></Textarea>
          <Button
            className="mt-3"
            variant="gradient"
            color="light-blue"
            size="lg"
            onClick={() => {
              if (task.reward) {
                submitTask();
              }
            }}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Addreward;
