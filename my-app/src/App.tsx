import React, { useState, useEffect } from "react";

interface LapsResponse {}

interface Members {
  members: number[];
  number: number;
}

function App() {
  const [data, setData] = useState<Members>({ members: [], number: 0 });
  const [myArray, setMyArray] = useState([{}]);

  // useEffect(() => {
  //   fetch(process.env.REACT_APP_API_HOST + "api/laps/15")
  //     .then((response) => response.json())
  //     .then((json) => console.log(json));
  // }, []);

  return (
    //Något e knas här bre!!!!!!
    <div>
      {typeof data.members === "undefined" ? (
        <p>Loading...</p>
      ) : (
        data.members.map((member: number, i) => <p key={i}>{member}</p>)
      )}
    </div>
  );
}

export default App;
