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
    <div style={{ textAlign: "left" }}>
      <p>
        <p style={{ fontWeight: "bold" }}>Username:</p> {convertStats["username"]["data"] ? convertStats["username"]["data"] : "Username not available"}
        <br /><br />
        <p style={{ fontWeight: "bold" }}>Movies watched in 2024:</p> {convertStats["2024_watch"]["data"] ? convertStats["2024_watch"]["data"] : "Watch count not available"}
        <br /><br />
        <p style={{ fontWeight: "bold" }}>Review Count:</p> {convertStats["review_count"]["data"] ? convertStats["review_count"]["data"] : "Review Count not available"}        
        <br /><br />
        <p style={{ fontWeight: "bold" }}>Average Movie Rating:</p> {convertStats["avg_rating"]["data"] ? convertStats["avg_rating"]["data"] : "Average Rating not available"}        
        <br /><br />
        <p style={{ fontWeight: "bold" }}>Standard Deviation:</p> {convertStats["std_dev"]["data"] ? convertStats["std_dev"]["data"] : "Standard Deviation not available"}        
        <br /><br /> 
        <p style={{ fontWeight: "bold" }}>Top Directors:</p>
        {convertStats["top_directors"]["data"] && convertStats["top_directors"]["data"].length > 0 ? (
            <div>
            {convertStats["top_directors"]["data"].map((take, index) => (
                <div>
                <p>{take.name} with {take.counts} movies watched</p>
                </div>
            ))}
            </div>
        ) : (
            <p>Top Directors not available</p>
        )}
        <br /><br />
        <p style={{ fontWeight: "bold" }}>"Hot Take" movies (your rating is more than 3 stars different than the average rating):</p>
        {/* Hot Takes: {convertStats["hot_takes"]["data"] ? convertStats["hot_takes"]["data"] : "Hot Takes not available"}         */}
        {convertStats["hot_takes"]["data"] && convertStats["hot_takes"]["data"].length > 0 ? (
            <div>
            {convertStats["hot_takes"]["data"].map((take, index) => (
                <div>
                <p>{take.film}:</p>
                <ul>
                <p>User Rating: {take.user_rating}</p>
                <p>Movie Rating: {take.movie_rating}</p>
                </ul>
                </div>
            ))}
            </div>
        ) : (
            <p>No hot takes available</p>
        )}


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
