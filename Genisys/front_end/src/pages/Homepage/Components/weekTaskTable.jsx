import React, { useEffect } from "react";
import { GetReq, PostReq } from "../../../HelperFunction/PostFunction";
import axios from "axios";

const WeekTaskTable = ({ task, deleteFun }) => {
  return (
    <div className="w-full flex flex-col bg-white rounded-xl shadow px-7 py-3 mt-5 min-h-80 ">
      <h1 className="font-bold text-xl">Last logs</h1>
      <table className=" w-full mt-6 ">
        <tr className="text-base text-gray-700  ">
          <th>Day</th>
          <th>Task</th>
          <th>Status</th>
          <th>Reward</th>
          <th>Action</th>
        </tr>
        {task.slice(0, 10).map((e) => (
          <tr className="border-b-2 border-blue-100 mt-1 font-normal  ">
            <th className="py-5 flex flex-col ">
              <h1>
                {Date(e.created_at).split(" ").slice(0, 1)}{" "}
                {Date(e.created_at).split(" ").slice(1, 2)}{" "}
                {Date(e.created_at).split(" ").slice(2, 3)}
              </h1>
              {/* <h1 className="font-normal">Happy </h1> */}
            </th>
            <th>{e.task}</th>
            <th className="py-5 flex justify-center">
              <p className="bg-green-200 text-green-700 rounded-full w-fit px-3 py-1 font-normal">
                Completed
              </p>
            </th>
            <th className="py-5 ">{e.reward}</th>
            <th className="py-5 flex justify-center items-end">
              <svg
                onClick={() => deleteFun(e.id)}
                id="Trash_Can_24"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
                //   xmlns:xlink="http://www.w3.org/1999/xlink"
              >
                <rect
                  width="24"
                  height="24"
                  stroke="none"
                  fill="#000000"
                  opacity="0"
                />

                <g transform="matrix(1 0 0 1 12 12)">
                  <path
                    transform=" translate(-12, -12)"
                    d="M 10 2 L 9 3 L 4 3 L 4 5 L 7 5 L 17 5 L 20 5 L 20 3 L 15 3 L 14 2 L 10 2 z M 5 7 L 5 20 C 5 21.1 5.9 22 7 22 L 17 22 C 18.1 22 19 21.1 19 20 L 19 7 L 5 7 z"
                    stroke-linecap="round"
                  />
                </g>
              </svg>
            </th>
          </tr>
        ))}
      </table>
    </div>
  );
};

export default WeekTaskTable;
