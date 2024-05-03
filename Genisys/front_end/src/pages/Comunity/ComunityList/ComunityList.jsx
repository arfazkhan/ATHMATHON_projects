import { Button, Input } from "@material-tailwind/react";
import axios from "axios";
import React, { useEffect, useState } from "react";
import {
  GetReq,
  PatchReq,
  PostReq,
} from "../../../HelperFunction/PostFunction";
import { Link } from "react-router-dom";

const ComunityList = () => {
  //   const [seach, setseach] = useState("");
  const [CommunityName, setCommunityName] = useState("");
  const [community, setcommunity] = useState([]);
  const [SeachList, setSeachList] = useState(false);
  const [createPop, setcreatePop] = useState(false);
  const [trigger, Settrigger] = useState(true);
  const searchList = async (data) => {
    try {
      const res = await GetReq(`community/?name=${data}`);
      setSeachList(res);
      console.log(res);
    } catch (error) {
      console.log(error);
    }
  };

  const joinCommunity = async (id) => {
    console.log(id);
    const res = await PatchReq(`community/?id=${id}`);
    console.log(res);
    Settrigger(!trigger);
  };
  const createCommunity = async () => {
    if (CommunityName !== "") {
      const res = await PostReq("community/", { name: CommunityName });
      if (res) {
        setCommunityName("");
        setcreatePop(false);
      }
    }
  };
  useEffect(() => {
    const getCommunity = async () => {
      const res = await GetReq(`community/?my=1`);
      setcommunity(res);
      setSeachList(false);
      console.log(res);
    };
    getCommunity();
  }, [setSeachList, createPop, trigger]);
  return (
    <div className="flex flex-col py-3 px-3 z-20 min-h-screen">
      <div className="">
        <div className="flex w-full justify-between items-center gap-3 ">
          <div className=""></div>

          <div className="flex gap-2">
            {SeachList ? (
              <div className="absolute top-0 w-full h-screen left-0 flex justify-center items-start pt-36">
                <div className="flex flex-col bg-white w-1/2 items-center px-7 py-5 rounded-md">
                  <div
                    className="flex justify-end w-full mb-4"
                    onClick={() => setSeachList(false)}
                  >
                    <svg
                      className="hover:bg-gray-50"
                      fill="none"
                      viewBox="0 0 24 24"
                      height="1.5em"
                      width="1.5em"
                    >
                      <path
                        fill="currentColor"
                        d="M16.34 9.322a1 1 0 10-1.364-1.463l-2.926 2.728L9.322 7.66A1 1 0 007.86 9.024l2.728 2.926-2.927 2.728a1 1 0 101.364 1.462l2.926-2.727 2.728 2.926a1 1 0 101.462-1.363l-2.727-2.926 2.926-2.728z"
                      />
                      <path
                        fill="currentColor"
                        fillRule="evenodd"
                        d="M1 12C1 5.925 5.925 1 12 1s11 4.925 11 11-4.925 11-11 11S1 18.075 1 12zm11 9a9 9 0 110-18 9 9 0 010 18z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  {SeachList.map((e) => (
                    <div className="flex justify-between w-full border-2 border-dashed border-blue-100 px-4 py-2 rounded-lg items-center mb-2">
                      {" "}
                      <h1 className="font-bold text-lg">{e.name} </h1>
                      <Button
                        onClick={() => joinCommunity(e.id)}
                        variant="gradient"
                        color="light-blue"
                        className="rounded-full"
                      >
                        Join
                      </Button>
                    </div>
                  ))}
                </div>{" "}
              </div>
            ) : (
              <></>
            )}{" "}
            <input
              type="text"
              placeholder="Search"
              className=" w-[400px] h-11 rounded-full outline-none px-4 shadow"
              onChange={(e) => searchList(e.target.value)}
            />
            <div className=" bg-white px-3 py-2 rounded-full shadow ">
              <svg
                fill="currentColor"
                viewBox="0 0 16 16"
                height="1.5rem"
                width="1.5rem"
              >
                <path d="M11.742 10.344a6.5 6.5 0 10-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 001.415-1.414l-3.85-3.85a1.007 1.007 0 00-.115-.1zM12 6.5a5.5 5.5 0 11-11 0 5.5 5.5 0 0111 0z" />
              </svg>
            </div>
          </div>
          <div
            className="bg-white px-3 py-1 rounded-xl items-center gap-2 flex font-semibold shadow"
            onClick={() => setcreatePop(true)}
          >
            <svg
              viewBox="0 0 1024 1024"
              fill="currentColor"
              height="2em"
              width="2em"
            >
              <path d="M696 480H544V328c0-4.4-3.6-8-8-8h-48c-4.4 0-8 3.6-8 8v152H328c-4.4 0-8 3.6-8 8v48c0 4.4 3.6 8 8 8h152v152c0 4.4 3.6 8 8 8h48c4.4 0 8-3.6 8-8V544h152c4.4 0 8-3.6 8-8v-48c0-4.4-3.6-8-8-8z" />
              <path d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z" />
            </svg>
            <h1>Create community</h1>
          </div>
        </div>
        {createPop ? (
          <div className="absolute w-full h-screen flex justify-center items-center top-0 left-0 backdrop-blur-sm">
            <div className="flex bg-white flex-col px-10 py-5 gap-3 rounded-xl">
              <h1 className="font-semibold text-xl">
                Create your own community
              </h1>
              <Input
                type="text"
                label="Community name"
                value={CommunityName}
                onChange={(e) => setCommunityName(e.target.value)}
              />
              <div className="flex gap-2">
                {" "}
                <Button
                  variant="gradient"
                  color="light-blue"
                  onClick={createCommunity}
                >
                  {" "}
                  Create{" "}
                </Button>
                <Button
                  variant="gradient"
                  color="red"
                  onClick={() => setcreatePop(false)}
                >
                  {" "}
                  Cancel{" "}
                </Button>
              </div>
            </div>
          </div>
        ) : (
          <></>
        )}
      </div>
      <div className="flex flex-col gap-3 mt-8 px-14">
        <h1 className="font-bold text-2xl">Joined community</h1>
        {community ? (
          community.map((e) => (
            <Link to={`/home/community/${e.id}`}>
              <div className="flex border-2 border-dashed border-blue-100 rounded-xl px-7 py-4 hover:bg-blue-50     ">
                <div className="">
                  <h1 className="font-bold text-xl">{e.name} </h1>
                  <h1>{e.people} members</h1>
                </div>
              </div>
            </Link>
          ))
        ) : (
          <></>
        )}
      </div>
    </div>
  );
};

export default ComunityList;
