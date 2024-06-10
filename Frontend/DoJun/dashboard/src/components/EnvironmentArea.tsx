import { Col, Row, Typography } from 'antd';
import { Environment, Event } from '../data';
import EnvironmentStatisticsCard from './EnvironmentStatisticCard';
import AlertCard from './AlertCard';
import EventCard from './EventCard';

interface EnvironmentAreaProps {
  currentEnvironmentData?: Environment;
  allEnvironmentData?: Environment[];
  allEvents?: Event[];
}

function EnvironmentArea(props: EnvironmentAreaProps) {
  const { currentEnvironmentData, allEnvironmentData, allEvents = [] } = props;
  const { Title } = Typography;

  const icons = {
    temperature: 'device_thermostat',
    light: 'fluorescent',
    co2Concentration: 'wifi_add',
    irrigation: 'humidity_high',
  };

  const alerts: {
    direction: 'up' | 'down';
    text: string;
    icon: string;
    date: string;
  }[] = [];
  if (allEnvironmentData) {
    for (let i = allEnvironmentData.length - 1; i > 0; i--) {
      for (const key of Object.keys(allEnvironmentData[0]) as Array<
        'date' | 'temperature' | 'fluorescents' | 'co2Concentration' | 'irrigation'
      >) {
        if (key === 'date') {
          continue;
        }
        if (allEnvironmentData[i][key] > allEnvironmentData[i - 1][key] * 1.1) {
          alerts.push({
            direction: 'up',
            text: `Rise in ${key}`,
            icon: icons[key],
            date: allEnvironmentData[i].date,
          });
        }
        if (allEnvironmentData[i][key] < allEnvironmentData[i - 1][key] * 0.9) {
          alerts.push({
            direction: 'down',
            text: `Fall in ${key}`,
            icon: icons[key],
            date: allEnvironmentData[i].date,
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
      <Row gutter={[8, 8]}>
        <Col span={8}>
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
        <Col span={8}>
          <EnvironmentStatisticsCard
            icon='fluorescent'
            text='Light'
            value={<>{currentEnvironmentData?.fluorescents ?? 0} </>}
          />
        </Col>
        <Col span={8}>
          <EnvironmentStatisticsCard
            icon='humidity_percentage'
            text='Humidity.'
            value={<>{currentEnvironmentData?.co2Concentration ?? 0} %</>}
          />
        </Col>
        <Col span={8}>
          <EnvironmentStatisticsCard
            icon='water_full'
            text='WaterLevel'
            value={<>{currentEnvironmentData?.irrigation ?? 0} %</>}
          />
        </Col>

        <Col span={8}>
          <EnvironmentStatisticsCard
            icon='water'
            text='SoilHumidity'
            value={<>{currentEnvironmentData?.irrigation ?? 0} %</>}
          />
        </Col>
        <Col span={8}>
          <EnvironmentStatisticsCard
            icon='rainy'
            text='Steam'
            value={<>{currentEnvironmentData?.irrigation ?? 0} %</>}
          />
        </Col>
      </Row>
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
