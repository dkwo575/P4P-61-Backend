import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

export default function ListData() {
  const [iot, setiot] = useState([]);

  useEffect(() => {
    getData();
  }, []);

  function getData() {
    axios
      .get("http://localhost:5000/api/data")
      .then((response) => {
        console.log(response.data);
        setiot(response.data);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }

  return (
    <div>
      <div className="container h-100">
        <div className="row h-100">
          <div className="col-12">
            <h1> The IoT sensor data list</h1>
            <table className="table table-bordered table-striped">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Temperature</th>
                  <th>Humidity</th>
                  <th>Light</th>
                  <th>WaterLevel</th>
                  <th>SoilHumidity</th>
                  <th>Steam</th>
                  <th>DateTime</th>
                </tr>
              </thead>
              <tbody>
                {iot.map((datas, key) => (
                  <tr key={key}>
                    <td>{datas.id}</td>
                    <td>{datas.temperature}</td>
                    <td>{datas.humidity}</td>
                    <td>{datas.light}</td>
                    <td>{datas.waterLevel}</td>
                    <td>{datas.soilHumidity}</td>
                    <td>{datas.steam}</td>
                    <td>{datas.datetime}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
