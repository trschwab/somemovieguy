import React from "react";

const StatsDisplay = ({ stats }) => {
  if (!stats) return <p>No stats available.</p>;

    // console.log(stats);
    // console.log(typeof stats);
    const convertStats = JSON.parse(stats);
    // console.log(convertStats);
    // console.log(typeof convertStats);

  // Convert the stats object to a nicely formatted JSON string
//   const formattedStats = JSON.stringify(stats, null, 2); // 2 spaces for indentation
//   const formattedJson = JSON.rawJSON(stats)

  return (
    <div>
      <p>
        Username: {convertStats["username"]["data"] ? convertStats["username"]["data"] : "Username not available"}
        <br />
        Movies watched in 2024: {convertStats["2024_watch"]["data"] ? convertStats["2024_watch"]["data"] : "Watch count not available"}
        <br />
        Average Movie Rating: {convertStats["avg_rating"]["data"] ? convertStats["avg_rating"]["data"] : "Average Rating not available"}        
        <br />
        Standard Deviation: {convertStats["std_dev"]["data"] ? convertStats["std_dev"]["data"] : "Standard Deviation not available"}        
        <br />
        Top Directors: {convertStats["top_directors"]["data"] ? convertStats["top_directors"]["data"] : "Top Directors not available"}        
        <br />
        Review Count: {convertStats["review_count"]["data"] ? convertStats["review_count"]["data"] : "Review Count not available"}        
        <br />
        Hot Takes: {convertStats["hot_takes"]["data"] ? convertStats["hot_takes"]["data"] : "Hot Takes not available"}        



      {/* {
  Object.entries(convertStats).map(([key, value], index) => (
    <div key={index}>
      {typeof value === 'object' ? (
        <>
          <p>{value.description}: </p>
          <p>{value.data}</p>
          
        </>
      ) : (
        <p>{value}</p>
      )}
    </div>
  ))
} */}



      </p>

    </div>
  );
};

export default StatsDisplay;
