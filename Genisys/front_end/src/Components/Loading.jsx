import React from "react";
import loading from "../Components/lottie/loading.json";
import Lottie from "lottie-react";
const Loading = () => {
  return <Lottie animationData={loading} className="w-1/3" />;
};

export default Loading;
