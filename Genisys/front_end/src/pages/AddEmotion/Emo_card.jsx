import Lottie from "lottie-react";
import React, { useRef } from "react";

const EmoCard = ({ anime, name, setactive }) => {
  const active = useRef(null);
  return (
    <div>
      <div
        className="flex bg-white justify-center items-center w-64 h-64 flex-col rounded-xl border-black "
        ref={active}
        onClick={() => setactive(active.current)}
      >
        <Lottie animationData={anime} className="w-2/3" />
        <h1 className="font-bold text-xl">{name}</h1>
      </div>
    </div>
  );
};

export default EmoCard;
