import Lottie from "lottie-react";
import React, { useEffect, useState } from "react";
import Wave from "../../Components/lottie/wave-anime.json";
import LeaderBoardCard from "../../Components/leaderBoardCard";
import { Card, Typography } from "@material-tailwind/react";
import TopThreeCard from "../../Components/topThree";
import { Link, useParams } from "react-router-dom";
import { GetReq } from "../../HelperFunction/PostFunction";

function ComunityPage() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const response = await GetReq(`community/?id=${id}`);
      setData(response);
      console.log(response);
      setLoading(false);
    })();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div className="w-full min-h-screen bg-gradient-to-t from-cyan-200 to-slate-50 relative">
      <Card variant="gradient" color="amber" className="mt-10 z-10 mx-10">
        <div className="p-10">
          <p className="text-4xl font-semibold text-center">{data.name}</p>
          <p className="font-medium text-center">
            Total points: {data.total_points}
          </p>
        </div>
      </Card>
      <Typography className="ml-10 font-semibold text-2xl mt-4">
        Leaderboard
      </Typography>
      <div className="mt-6 mx-10 flex gap-5 justify-center">
        {data.users.slice(0, 3).map((user, index) => (
          <TopThreeCard
            name={user.username}
            score={user.points}
            postion={index + 1}
            key={index}
            image={user.image}
            id={user.id}
          />
        ))}
      </div>
      <div className="w-full px-10 mt-10 flex flex-col gap-5">
        {data.users.length > 3 &&
          data.users.map((user, index) => (
            <LeaderBoardCard
              id={user.id}
              name={user.username}
              key={index}
              position={index + 1}
              image={user.image}
              points={user.points}
            />
          ))}
      </div>
      <Lottie animationData={Wave} className=" absolute bottom-0 w-full" />
    </div>
  );
}

export default ComunityPage;
