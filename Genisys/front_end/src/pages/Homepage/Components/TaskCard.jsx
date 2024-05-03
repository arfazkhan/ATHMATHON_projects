import Lottie from "lottie-react";
import React, { useEffect, useState } from "react";
import complete from "../../../Components/lottie/rewardCelebration.json";
import axios from "axios";
import { useAtom } from "jotai";
import { triggerAtom } from "../../../GlobelState";
import { PatchReq } from "../../../HelperFunction/PostFunction";
const TaskCard = ({ task }) => {
  const [trigger, SetTrigger] = useAtom(triggerAtom);
  const [completePop, setcompletePop] = useState(false);
  const [Tips, setTips] = useState(false);
  const completeTask = async (id) => {
    setcompletePop(true);
    const res = await PatchReq("task/", { id });

    setTimeout(function () {
      setcompletePop(false);
      SetTrigger(trigger ? false : true);
    }, 3000);
  };

  const connectAi = async (task) => {
    const data = {
      contents: [
        {
          parts: [
            {
              text: `Give four tips for ${task} , tips are separated by "," and put them in a array "[]" `,
            },
          ],
        },
      ],
    };

    const headers = {
      "Content-Type": "application/json",
    };
    const res = await axios.post(
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyCXvY9PiKl2FFl2shCBQMysncurdiz1WUk",
      data,
      { headers }
    );
    const response = res.data.candidates;
    console.log(response);
    if (response) {
      if (response[0].content) {
        setTips(response[0].content.parts);
      }
    }
  };
  const [quate, setquate] = useState("");
  useEffect(() => {
    const getQuote = async () => {
      try {
        const res = await axios.get("https://type.fit/api/quotes");
        const data = res.data;
        const randomIndex = Math.floor(Math.random() * data.length);
        const randomQuote = data[randomIndex];
        setquate(randomQuote);
      } catch (error) {
        console.error("Error fetching quote:", error);
      }
    };
    getQuote();
  }, []);
  return (
    <div className="border-b-2  pb-5 mt-4 relative">
      {completePop ? <Complete_Reward_pop /> : <></>}
      <h1 className="font-bold text-2xl">{task.task}</h1>

      <div className="grid grid-cols-2">
        <div>
          <div className="flex gap-2">
            <h1 className="bg-red-200 px-3 text-sm font-semibold py-1 rounded-full  mt-3 flex items-center gap-1">
              <svg
                id="Clock_24"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <rect
                  width="24"
                  height="24"
                  stroke="none"
                  fill="#000000"
                  opacity="0"
                />

                <g transform="matrix(0.83 0 0 0.83 12 12)">
                  <path
                    transform=" translate(-16, -16)"
                    d="M 16 4 C 9.382813 4 4 9.382813 4 16 C 4 22.617188 9.382813 28 16 28 C 22.617188 28 28 22.617188 28 16 C 28 9.382813 22.617188 4 16 4 Z M 16 6 C 21.535156 6 26 10.464844 26 16 C 26 21.535156 21.535156 26 16 26 C 10.464844 26 6 21.535156 6 16 C 6 10.464844 10.464844 6 16 6 Z M 15 8 L 15 17 L 22 17 L 22 15 L 17 15 L 17 8 Z"
                    stroke-linecap="round"
                  />
                </g>
              </svg>
              {task.expire_min}
              {" mins "}
            </h1>
            <p className="bg-green-200  px-3 py-1 rounded-full text-sm font-semibold mt-3">
              Reward : {task.reward}
            </p>
          </div>

          <div className=" max-w-lg mt-8 text-sm ">
            <h1>
              <i>{quate.text}</i>
            </h1>

            <i className="ml-5">
              -{quate.author ? quate.author.split(",")[0] : ""}
            </i>
          </div>
          <div className="flex mt-2 gap-2">
            {/* <Button
      variant="gradient"
      color="light-green"
      // className="rounded-full"
    >
      I'm Done
    </Button> */}
            <button
              className="bg-green-100 text-green-500 px-7 py-2 rounded-lg font-bold "
              onClick={() => completeTask(task.id)}
            >
              {" "}
              I'm Done
            </button>
            <button
              className="bg-blue-100 text-blue-500 px-7 py-2 rounded-lg flex items-center gap-1"
              onClick={() => connectAi(task.task)}
            >
              {" "}
              <h1 className=" font-bold">Learn How</h1>{" "}
              <svg
                viewBox="0 0 1024 1024"
                fill="currentColor"
                height="1.5em"
                width="1.5em"
              >
                <path d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm144.1 454.9L437.7 677.8a8.02 8.02 0 01-12.7-6.5V353.7a8 8 0 0112.7-6.5L656.1 506a7.9 7.9 0 010 12.9z" />
              </svg>
            </button>
          </div>
        </div>
        <div className="">
          {" "}
          {Tips ? (
            <div>
              <h1>Tips</h1>
              {JSON.parse(Tips[0].text).map((e) => (
                <li>{e}</li>
              ))}
            </div>
          ) : (
            <></>
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskCard;

const Complete_Reward_pop = () => {
  return (
    <>
      <div className="flex absolute left-0 w-full  justify-center items-center top-0 z-10">
        <Lottie animationData={complete} className="w-1/4 h-1/4 " />
      </div>
    </>
  );
};
