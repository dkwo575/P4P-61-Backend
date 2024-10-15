import { Col, Row, Typography, Button, DatePicker, Select } from 'antd';
// import { Environment, Event } from '../data';
import EnvironmentStatisticsCard from './EnvironmentStatisticCard';
import AlertCard from './AlertCard';
import EventCard from './EventCard';
import axios, { all } from 'axios';
import { useEffect, useState } from 'react';
import { set } from 'lodash-es';

const { Option } = Select;

interface EnvironmentAreaProps {
  currentEnvironmentData?: Environment[];
  allEnvironmentData?: Environment[];
  allEvents?: Event[];
}

interface Environment {
  id: number;
  temperature: number;
  humidity: number;
  light: number;
  waterLevel: number;
  soilHumidity: number;
  steam: number;
  datetime: string;
}

interface Event {
  date: string;
  text: string;
}

function EnvironmentArea(props: EnvironmentAreaProps) {
  // const { currentEnvironmentData, allEnvironmentData, allEvents = [] } = props;
  // const { Title } = Typography;

  const [allEnvironmentData, setAlleEnvironmentData] = useState<Environment[]>([]);
  const [currentEnvironmentData, setCurrentEnvironmentData] = useState<Environment | null>(null);
  const [allEvents, setAllEvents] = useState<Event[]>([]);
  // const [selectDate, setSelectDate] = useState<moment.Moment | null>(null);
  const [currentId, setCurrentId] = useState<number>(1);
  const [dateTimes, setDateTimes] = useState<string[]>([]);

  const { Title } = Typography;

  const icons = {
    temperature: 'device_thermostat',
    light: 'fluorescent',
    humidity: 'humidity_percentage',
    waterLevel: 'humidity_high',
    soilHumidity: 'water',
    steam: 'rainy',
  };
  // create new function fetchEnvironmentData

  // const fetchEnvironmentData = async () => {
  //   const response = await axios.get('http://localhost:5000/api/data');
  //   setAlleEnvironmentData(response.data);
  //   setCurrentEnvironmentData(response.data[response.data.length - 1]);
  // };

  // useEffect(() => {
  //   fetchEnvironmentData();
  // });

  const fetchEnvironmentDataID = async (id: number) => {
    const response = await axios.get(`http://localhost:5000/api/data/${id}`);
    setCurrentEnvironmentData(response.data);
  };

  const fetchAllDateTimes = async () => {
    const response = await axios.get('http://localhost:5000/api/data');
    setAlleEnvironmentData(response.data);
    const dateTimes = response.data.map((data: Environment) => data.datetime);
    setDateTimes(dateTimes);
  };

  useEffect(() => {
    fetchEnvironmentDataID(currentId);
    fetchAllDateTimes();
  }, [currentId]);

  const handleNext = () => {
    if (currentId < allEnvironmentData.length) {
      setCurrentId(currentId + 1);
    }
  };

  const handlePrev = () => {
    if (currentId > 1) {
      setCurrentId(currentId - 1);
    }
  };

  const handleTimeChange = (value: string) => {
    const index = dateTimes.indexOf(value);
    if (index !== -1) {
      setCurrentId(index + 1);
    }
  };

  // old function
  const alerts: {
    direction: 'up' | 'down';
    text: string;
    icon: string;
    date: string;
  }[] = [];
  if (allEnvironmentData) {
    for (let i = allEnvironmentData.length - 1; i > 0; i--) {
      for (const key of Object.keys(allEnvironmentData[0]) as Array<
        // 'date' | 'temperature' | 'fluorescents' | 'co2Concentration' | 'irrigation'
        'datetime' | 'temperature' | 'humidity' | 'light' | 'waterLevel' | 'soilHumidity' | 'steam'
      >) {
        if (key === 'datetime' || key === 'id') {
          // (key === 'date')
          continue;
        }
        if (allEnvironmentData[i][key] > allEnvironmentData[i - 1][key] * 1.1) {
          alerts.push({
            direction: 'up',
            text: `Rise in ${key}`,
            icon: icons[key],
            date: allEnvironmentData[i].datetime,
          });
        }
        if (allEnvironmentData[i][key] < allEnvironmentData[i - 1][key] * 0.9) {
          alerts.push({
            direction: 'down',
            text: `Fall in ${key}`,
            icon: icons[key],
            date: allEnvironmentData[i].datetime,
          });
        }
      }
    }
  }

  const handleScroll = (event: WheelEvent) => {
    const container = event.currentTarget as Element;
    const scrollAmount = event.deltaY;
    container.scrollTo({
      top: 0,
      left: container.scrollLeft + scrollAmount,
      behavior: 'auto',
    });
  };

  return (
    <>
      <Row>
        <Col>
          <Title level={4} style={{ marginTop: 20 }}>
            Environment(IoT sensor)
          </Title>
        </Col>
      </Row>

      <Row>
        <Col span={8}>
          <Button onClick={handlePrev} disabled={currentId <= 1}>
            Previous
          </Button>
        </Col>
        <Col span={8} style={{ textAlign: 'center' }}>
          <Select
            style={{ width: '100%' }}
            value={currentEnvironmentData?.datetime}
            onChange={handleTimeChange}
          >
            {dateTimes.map((datetime) => (
              <Option key={datetime} value={datetime}>
                {datetime}
              </Option>
            ))}
          </Select>
        </Col>
        <Col span={8} style={{ textAlign: 'right' }}>
          <Button onClick={handleNext} disabled={currentId >= allEnvironmentData.length}>
            Next
          </Button>
        </Col>
      </Row>

      <Row gutter={[8, 8]}>
        <Col span={12}>
          <EnvironmentStatisticsCard
            icon='device_thermostat'
            text='Tempurature'
            value={
              <>
                {currentEnvironmentData?.temperature ?? 0} <sup>o</sup>C
              </>
            }
          />
        </Col>
        <Col span={12}>
          <EnvironmentStatisticsCard
            icon='humidity_percentage'
            text='Humidity'
            value={<>{currentEnvironmentData?.humidity ?? 0} %</>}
          />
        </Col>
        <Col span={12}>
          <EnvironmentStatisticsCard
            icon='fluorescent'
            text='Light.'
            value={<>{currentEnvironmentData?.light ?? 0} </>}
          />
        </Col>
        <Col span={12}>
          <EnvironmentStatisticsCard
            icon='water_full'
            text='WaterLevel'
            value={<>{currentEnvironmentData?.waterLevel ?? 0} %</>}
          />
        </Col>
      </Row>

      <Row gutter={[12, 12]}>
        <Col span={12}>
          <EnvironmentStatisticsCard
            icon='water'
            text='SoilHumidity'
            value={<>{currentEnvironmentData?.soilHumidity ?? 0} %</>}
          />
        </Col>
        <Col span={12}>
          <EnvironmentStatisticsCard
            icon='rainy'
            text='Steam'
            value={<>{currentEnvironmentData?.steam ?? 0} %</>}
          />
        </Col>
        <Col span={12}>
          <EnvironmentStatisticsCard
            icon='date_range'
            text='Date'
            value={<>{currentEnvironmentData?.datetime ?? 'No date'}</>}
          />
        </Col>
      </Row>
      {/* <Row>
        <Col span={8}>
          <Button onClick={handlePreviousDate}>Previous Day</Button>
        </Col>
        <Col span={8} style={{ textAlign: 'center' }}>
          <DatePicker
            showTime
            value={selectDate}
            onChange={handleDateChange}
            format='YYYY-MM-DD HH:mm:ss'
          />
        </Col>
        <Col span={8} style={{ textAlign: 'right' }}>
          <Button onClick={handleNextDate}>Next Day</Button>
        </Col>
      </Row> */}
      <Row>
        <Col>
          <Title level={4} style={{ marginTop: 20 }}>
            Alerts
          </Title>
        </Col>
      </Row>
      <Row>
        <Col
          span={24}
          style={{ display: 'flex', gap: 8, overflowX: 'auto' }}
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-ignore
          onWheel={handleScroll}
        >
          {alerts.map((alert) => (
            <AlertCard key={alert.date} {...alert} />
          ))}
        </Col>
      </Row>
      <Row>
        <Col>
          <Title level={4} style={{ marginTop: 20 }}>
            Events
          </Title>
        </Col>
      </Row>
      <Row>
        <Col
          span={24}
          style={{ display: 'flex', gap: 8, overflowX: 'auto' }}
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-ignore
          onWheel={handleScroll}
        >
          {allEvents.map((event) => (
            <EventCard key={event.date} {...event} />
          ))}
        </Col>
      </Row>
    </>
  );
}

export default EnvironmentArea;
