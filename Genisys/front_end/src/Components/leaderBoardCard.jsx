import { Card, Typography } from "@material-tailwind/react";
import React from "react";
import { Link } from "react-router-dom";

function LeaderBoardCard({ name, image, points, position, id }) {
  return (
    <Link to={`/home/profile/${id}`}>
      <Card className="px-5 py-2 z-10" color="light-blue">
        <div className="flex gap-10 items-center">
          <p className="rounded-full bg-blue-700 h-[30px] w-[30px] flex justify-center items-center text-white">
            {position}
          </p>
          <div className="w-[50px] h-[35px]">
            <img src={image} alt="" className="w-full rounded-full h-full" />
          </div>
          <p className="w-full font-medium">{name}</p>
          <Typography color="white" className="font-bold">
            {points}
          </Typography>
        </div>
      </Card>
    </Link>
  );
}

export default LeaderBoardCard;
