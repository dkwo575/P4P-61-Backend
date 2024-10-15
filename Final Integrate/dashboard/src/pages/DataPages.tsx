import theme from '../theme';
import col from 'antd/es/col';
import row from 'antd/es/row';
import { Link } from 'react-router-dom';
import React, { useEffect, useState } from 'react';
// import EnvironmentArea from '../components/EnvironmentArea';
import axios from 'axios';
import { set } from 'lodash-es';

export default function DataPages() {
  const [iot, setiot] = useState([]);

  const [filteredIot, setFilteredIot] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [sortField, setSortField] = useState('');
  const [sortOrder, setSortOrder] = useState('');

  // const [SortingCriteria, setSortingCriteria] = useState(null);
  // const [FilteringCriteria, setFilteringCriteria] = useState({
  //   startDate: '',
  //   endDate: '',
  //   type: '',
  // });

  useEffect(() => {
    getIoTData();
  }, []);

  useEffect(() => {
    filterAndSortData();
  }, [startDate, endDate, sortField, sortOrder]);

  useEffect(() => {
    convertTots();
  }, []);

  // useEffect(() => {
  //   handleFilter();
  // }, [FilteringCriteria, iot]);

  // useEffect(() => {
  //   if (SortingCriteria) {
  //     handleSort(SortingCriteria);
  //   }
  // }, [SortingCriteria, iot]);

  function getIoTData() {
    axios
      .get('http://localhost:5000/api/data')
      .then((response) => {
        console.log(response.data);
        setiot(response.data);
        setFilteredIot(response.data); // initialize filtered data
      })
      .catch((error) => {
        console.log(error);
      });
  }

  function convertTots() {
    axios.get('http://localhost:5000/save_json').then((response) => {
      console.log(response.data);
    });
  }

  function filterAndSortData() {
    let filteredData = iot;
    if (startDate && endDate) {
      filteredData = filteredData.filter((data) => {
        const dataDate = new Date(data.datetime);
        return dataDate >= new Date(startDate) && dataDate <= new Date(endDate);
      });
    }

    if (sortField) {
      filteredData = filteredData.sort((a, b) => {
        if (a[sortField] > b[sortField]) {
          return sortOrder === 'asc' ? 1 : -1;
        }
        if (a[sortField] < b[sortField]) {
          return sortOrder === 'asc' ? -1 : 1;
        }
        return 0;
      });
    }

    setFilteredIot(filteredData);
  }

  // function handleSort(criteria) {
  //   const sortedData = [...filteredIot].sort((a, b) => {
  //     if (a[criteria] > b[criteria]) {
  //       return 1;
  //     }
  //     if (a[criteria] < b[criteria]) {
  //       return -1;
  //     }
  //     return 0;
  //   });
  //   // setiot(sortedData);
  //   setSortingCriteria(criteria);
  //   setFilteredIot(sortedData);
  // }

  // function handleFilter() {
  //   const { startDate, endDate, type } = FilteringCriteria;
  //   let filteredData = iot;
  //   if (startDate) {
  //     filteredData = filteredData.filter((data) => new Date(data.datetime) >= new Date(startDate));
  //   }
  //   if (endDate) {
  //     filteredData = filteredData.filter((data) => new Date(data.datetime) >= new Date(endDate));
  //   }
  //   if (type) {
  //     filteredData = filteredData.filter((data) => data[type] === type);
  //   }
  // const filteredData = iot.filter((data) => {
  //   if (FilteringCriteria.startDate && data.datetime < FilteringCriteria.startDate) {
  //     return false;
  //   }
  //   if (FilteringCriteria.endDate && data.datetime > FilteringCriteria.endDate) {
  //     return false;
  //   }
  //   if (FilteringCriteria.type && data.type !== FilteringCriteria.type) {
  //     return false;
  //   }
  //   return true;
  // });
  //   setiot(filteredData);
  // }

  return (
    <div
      style={{
        height: 'calc(100vh - 120px)',
        overflow: 'auto',
        background: theme.palette.pumpkin1,
      }}
    >
      <div className='container h-100'>
        <div className='row h-100'>
          <div className='col-12'>
            <h1> The IoT sensor data list</h1>
            <div>
              <label>Sort by start date:</label>
              <input type='date' value={startDate} onChange={(e) => setStartDate(e.target.value)} />

              <label>Sort by end date:</label>
              <input type='date' value={endDate} onChange={(e) => setEndDate(e.target.value)} />

              <label>Sort by type:</label>
              <select
                value={sortField}
                onChange={
                  (e) => setSortField(e.target.value)
                  // setFilteringCriteria({ ...FilteringCriteria, type: e.target.valu})
                }
              >
                <option value=''>Selecct</option>
                <option value='temperature'>Temperature</option>
                <option value='humidity'>Humidity</option>
                <option value='light'>Light</option>
                <option value='waterLevel'>WaterLevel</option>
                <option value='soilHumidity'>SoilHumidity</option>
                <option value='steam'>Steam</option>
              </select>
              <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value)}>
                <option value='asc'>Ascending</option>
                <option value='desc'>Descending</option>
              </select>

              <button onClick={convertTots}>Convert to ts</button>
            </div>

            <table className='table table-bordered table-striped'>
              <thead>
                <tr>
                  <th>id number</th>
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
                {filteredIot.map((datas, key) => (
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
