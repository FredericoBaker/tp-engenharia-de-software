import { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      console.log(import.meta.env.VITE_API_URL);
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}`);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const result = await response.json();
        const postsResponse = await fetch(result.posts);
        const posts = await postsResponse.json();
        console.log(posts);

        setData(posts);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    fetchData();
  }, []);

  return (
    <>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
          width: "100%",
          
        }}
      >
        {data.map((item, index) => (
          <div
            key={index}
            style={{marginTop: "0.5rem"}}
          >
            {item.title}
          </div>
        ))}
      </div>
    </>
  );
}

export default App;
