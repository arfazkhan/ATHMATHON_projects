import React, { useState } from "react";
import Wave from "../../Components/lottie/wave-anime.json";
import Lottie from "lottie-react";
import Select_Category from "../Category/selectCategory";
import AddTask from "../AddTask/AddTask";
import Addreward from "../SelectReward/SelectReward";
import { PostReq } from "../../HelperFunction/PostFunction";
import { useNavigate } from "react-router-dom";
const Task = () => {
  const [currentScreen, setcurrentScreen] = useState("category");
  const navigate = useNavigate();
  const [task, settask] = useState({
    task: 0,
    reward: 0,
    category: 0,
    expire: 10,
  });
  const submitTask = async () => {
    const res = await PostReq("task/", task);
    if (res) {
      navigate("/home");
    }
  };
  let currentComponent;
  console.log(task);
  console.log(currentScreen);
  if (currentScreen === "category") {
    currentComponent = (
      <Select_Category
        change_screen={setcurrentScreen}
        Setstate={settask}
        task={task}
      />
    );
  } else if (currentScreen === "addtask") {
    currentComponent = (
      <AddTask
        change_screen={setcurrentScreen}
        Setstate={settask}
        task={task}
      />
    );
  } else {
    currentComponent = (
      <Addreward submitTask={submitTask} Setstate={settask} task={task} />
    );
  }
  return (
    <div className="w-full min-h-screen bg-gradient-to-t from-cyan-200 to-slate-50 relative flex  flex-col justify-center items-center ">
      {currentComponent}
      <Lottie animationData={Wave} className=" absolute bottom-0 w-full " />
    </div>
  );
};

export default Task;
