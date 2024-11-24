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
      <h3>User Stats</h3>
      <p>
      {
  Object.entries(convertStats).map(([key, value], index) => (
    <div key={index}>
      <p>{key}</p>
      {typeof value === 'object' ? (
        <>
          <p>Data: {value.data}</p>
          <p>Description: {value.description}</p>
        </>
      ) : (
        <p>{value}</p>
      )}
    </div>
  ))
}



      </p>

    </div>
  );
};

export default StatsDisplay;
