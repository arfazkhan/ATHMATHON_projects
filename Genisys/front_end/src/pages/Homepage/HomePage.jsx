import React, { useEffect, useState } from "react";
import Wave from "../../Components/lottie/wave-anime.json";
import Lottie from "lottie-react";
import { Button, useSelect } from "@material-tailwind/react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { GetReq, PatchReq, PostReq } from "../../HelperFunction/PostFunction";

import learning from "../../Components/lottie/learning.json";
import relation from "../../Components/lottie/relation.json";
import fitness from "../../Components/lottie/fitness.json";
import cleaning from "../../Components/lottie/cleaning.json";
import career from "../../Components/lottie/career.json";
import funny from "../../Components/lottie/funny.json";
import TaskCard from "./Components/TaskCard";
import WeekTaskTable from "./Components/weekTaskTable";
import { StickyNavbar } from "../../Components/Nav/Navbar";
import Loading from "../../Components/Loading";
import { useAtom } from "jotai";
import { triggerAtom } from "../../GlobelState";

const HomePage = () => {
  const [trigger, setTrigger] = useAtom(triggerAtom);
  const [name, setname] = useState("");
  const [greetings, setgreeting] = useState("");

  const deleteHandle = async (id) => {
    const res = await PostReq("delete-task/", { id });
    console.log(res);
    setTrigger(!trigger);
  };
  const [taskData, settaskData] = useState([]);
  const [taskDataComplete, settaskDataComplete] = useState([]);
  const lastlog = localStorage.getItem("time");
  const navigate = useNavigate();

  useEffect(() => {
    const getuser = () => {
      const username = localStorage.getItem("user");
      setname(username);
    };
    const FunctiongetTask = async () => {
      const data = await GetReq("task/");
      // console.log(data);
      if (data) {
        settaskData(data.not_done);
      }
    };
    const FunctiongetTaskComplete = async () => {
      const data = await GetReq("task/");
      // console.log(data);
      if (data) {
        console.log(data.done);
        settaskDataComplete(data.done.reverse());
      }
    };
    function getGreeting() {
      const currentDate = new Date();
      const currentHour = currentDate.getHours();

      let greeting;

      if (currentHour >= 5 && currentHour < 12) {
        greeting = "Good morning!";
      } else if (currentHour >= 12 && currentHour < 18) {
        greeting = "Good afternoon!";
      } else if (currentHour >= 18 && currentHour < 22) {
        greeting = "Good evening!";
      } else {
        greeting = "Hello!";
      }

      return greeting;
    }

    // Example usage:
    const greeting = getGreeting();
    setgreeting(greeting);
    FunctiongetTask();
    FunctiongetTaskComplete();
    getuser();
  }, [trigger]);

  const navTask = () => {
    // Retrieve the last logged time from wherever it's stored
    const lastLogString = localStorage.getItem("lastLog");

    // Convert the stored string back to a Date object
    const lastLog = lastLogString ? new Date(lastLogString) : null;

    if (lastLog) {
      // Calculate the time difference in milliseconds
      const currentTime = new Date();
      const timeDiffMilliseconds = currentTime - lastLog;

      // Convert milliseconds to hours
      const timeDiffHours = timeDiffMilliseconds / (1000 * 60 * 60);
      if (timeDiffHours >= 4) {
        navigate("/home/addemo");
      } else {
        navigate("/home/addcat");
      }
    } else {
      navigate("/home/addemo");
    }
  };
  return (
    <>
      <div className="flex  flex-col gap-2 z-10 px-24 py-10 w-full">
        <div className=" border-2 border-blue-100 px-7 py-3 border-dashed w-full rounded-xl    relative ">
          {/* <Lottie animationData={Wave_2} /> */}
          <h1 className="font-black text-3xl poppins-bold">
            Hello {name.toLocaleUpperCase()},
          </h1>
          <h1 className="font-black text-3xl poppins-bold">{greetings}</h1>
          {/* <Link className="flex bg-blue-100 w-32 px-3 py-2 shadow">
            Start{" "}
            
          </Link> */}

          <Button
            onClick={() => navTask()}
            variant="gradient"
            color="light-blue"
            size="sm"
            className="text-xl flex gap-2 items-center mt-3"
          >
            Start
          </Button>
        </div>
        {/* Daily task section */}
        <div className="w-full flex flex-col bg-white rounded-xl shadow px-7 py-3 mt-5 min-h-80 justify-between">
          <h1 className="font-bold text-xl">Today's objectives</h1>

          <div className="mt-9">
            {taskData ? (
              taskData.length != 0 ? (
                taskData.map((e) => (
                  <>
                    <TaskCard task={e} />
                  </>
                ))
              ) : (
                <div className="flex flex-col w-full">
                  <Lottie animationData={funny} className="w-1/4" />
                  <h1 className="font-bold">It's empty , Add your emotion.</h1>

                  <div className="">
                    <Button
                      onClick={navTask}
                      variant="gradient"
                      color="light-blue"
                      size="sm"
                      className="text-xl flex gap-2 items-center mt-3"
                    >
                      Start
                    </Button>
                  </div>
                </div>
              )
            ) : (
              <Loading />
            )}
          </div>
          <div className="flex flex-col items-center">
            {/* <h1 className="text-2xl font-bold text-gray-700">
              Its empty here,Add your emotion.
            </h1> */}

            {/* <div className="">
              <Button
                variant="gradient"
                color="light-blue"
                size="sm"
                className="text-xl flex gap-2 items-center mt-3"
              >
                Start
              </Button>
            </div> */}
          </div>
        </div>
        {/* weekly task section  */}
        <WeekTaskTable task={taskDataComplete} deleteFun={deleteHandle} />
      </div>
    </>
  );
};

export default HomePage;
