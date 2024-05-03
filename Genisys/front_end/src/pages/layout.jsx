import React from "react";
import Wave from "../Components/lottie/wave-anime.json";

import stand from "../Character/stand.png";
import ask from "../Character/ask.png";
import think from "../Character/think.png";

import { StickyNavbar } from "../Components/Nav/Navbar";
import { Outlet } from "react-router-dom";
import Lottie from "lottie-react";
import axios from "axios";

const Layout = () => {
  return (
    <div className="w-full min-h-screen bg-gradient-to-t from-cyan-200 to-slate-50 relative flex justify-between  flex-col  ">
      <StickyNavbar />
      <Outlet />
      {/* <div className="absolute z-50 right-0 ">
        <img src={stand} alt="" />
      </div> */}

      <Lottie animationData={Wave} className=" absolute bottom-0 w-full " />
    </div>
  );
};

export default Layout;
