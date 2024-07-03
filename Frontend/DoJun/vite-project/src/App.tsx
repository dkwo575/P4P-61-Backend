import { useState, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

import { BrowserRouter, Route, Switch, Routes, Link } from "react-router-dom";
import { Button } from "react-bootstrap";

import ListData from "./pages/ListData";
// import DatabyDate from "./pages/DatabyDate";

function App() {
  // const [count, setCount] = useState(0);

  // const [data, setData] = useState([]);

  // useEffect(() => {
  //   axios
  //     .get("http://localhost:5000/api/data")
  //     .then((response) => {
  //       console.log(response.data);
  //       setData(response.data);
  //     })
  //     .catch((error) => console.error("Error fetching data:", error));
  // }, []);

  return (
    <div className="vh-100 gradient-custom">
      <div className="container">
        <h1 className="page-header text-center">
          React-JS and Python Flask CRUD Create, Read, Update and Delete
          MySql-Database
        </h1>
        <div>
          <h3 className="text-center">click button for move to data list</h3>
        </div>
        <div>
          {/* <p>
            <Link to="/list" className="btn btn-success">
              <button> List Data</button>
            </Link>
          </p> */}
          <button
            onClick={() => {
              location.href = "./list";
            }}
          >
            List Data
          </button>
        </div>

        <BrowserRouter>
          <Routes>
            <Route path="/list" element={<ListData />} />
          </Routes>
        </BrowserRouter>
      </div>
    </div>

    // {/* <ul>
    //   {data.map((item) => (
    //     <li key={item.id}>{item.temperature}</li>
    //   ))}
    // </ul> */}
    // <>
    //   <div>
    //     <a href="https://vitejs.dev" target="_blank">
    //       <img src={viteLogo} className="logo" alt="Vite logo" />
    //     </a>
    //     <a href="https://react.dev" target="_blank">
    //       <img src={reactLogo} className="logo react" alt="React logo" />
    //     </a>
    //   </div>
    //   <h1>Vite + React</h1>
    //   <div className="card">
    //     <button onClick={() => setCount((count) => count + 1)}>
    //       count is {count}
    //     </button>
    //     <p>
    //       Edit <code>src/App.tsx</code> and save to test HMR
    //     </p>
    //   </div>
    //   <p className="read-the-docs">
    //     Click on the Vite and React logos to learn more
    //   </p>
    // </>
  );
}

export default App;
