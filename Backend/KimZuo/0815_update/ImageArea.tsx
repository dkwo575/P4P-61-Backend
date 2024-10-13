import { useEffect, useState } from 'react';
import axios from 'axios';
import { Col, Row, Button, Select } from 'antd';
import theme from '../theme';

const { Option } = Select;

export default function ImagePage() {
  const [imageSrc, setImageSrc] = useState<string[]>([]);
  const [currentImage, setCurrentImage] = useState<string>('');
  const [currentIndex, setCurrentIndex] = useState<number>(0);

  const [imageSrc2, setImageSrc2] = useState<string[]>([]);
  const [resultImage, setResultImage] = useState<string>('');
  const [resultIndex, setResultIndex] = useState<number>(0);

  const [folders, setFolders] = useState<string[]>([]);
  const [selectedFolder, setSelectedFolder] = useState<string>('');
  const [resultFolders, setResultFolders] = useState<string[]>([]);
  const [selectedResultFolder, setSelectedResultFolder] = useState<string>('');

  useEffect(() => {
    getFolders();
    getResultFolders();
  }, []);

  useEffect(() => {
    if (selectedFolder) getImageData(selectedFolder);
  }, [selectedFolder]);

  useEffect(() => {
    if (selectedResultFolder) getResultImage(selectedResultFolder);
  }, [selectedResultFolder]);

  function getFolders() {
    axios.get('http://localhost:5000/api/subfolders?folder=Original')
      .then(response => {
        setFolders(response.data);
        if (response.data.length > 0) {
          setSelectedFolder(response.data[0]);
        }
      })
      .catch(error => console.log(error));
  }

  function getResultFolders() {
    axios.get('http://localhost:5000/api/subfolders?folder=Result')
      .then(response => {
        setResultFolders(response.data);
        if (response.data.length > 0) {
          setSelectedResultFolder(response.data[0]);
        }
      })
      .catch(error => console.log(error));
  }

  function getImageData(folder: string) {
    axios.get(`http://localhost:5000/api/files?folder=Original&subfolder=${folder}`)
      .then(response => {
        setImageSrc(response.data);
        if (response.data.length > 0) {
          setCurrentImage(response.data[0]);
          setCurrentIndex(0);
        }
      })
      .catch(error => console.log(error));
  }

  function getResultImage(folder: string) {
    axios.get(`http://localhost:5000/api/files?folder=Result&subfolder=${folder}`)
      .then(response => {
        setImageSrc2(response.data);
        if (response.data.length > 0) {
          setResultImage(response.data[0]);
          setResultIndex(0);
        }
      })
      .catch(error => console.log(error));
  }

  function runAIModel() {
    axios.get('http://localhost:5000/api/process')
      .then(response => console.log(response.data))
      .catch(error => console.log(error));
  }

  const nextImage = () => {
    if (currentIndex < imageSrc.length - 1) {
      const newIndex = currentIndex + 1;
      setCurrentIndex(newIndex);
      setCurrentImage(imageSrc[newIndex]);
    }
  };

  const prevImage = () => {
    if (currentIndex > 0) {
      const newIndex = currentIndex - 1;
      setCurrentIndex(newIndex);
      setCurrentImage(imageSrc[newIndex]);
    }
  };

  const nextResultImage = () => {
    if (resultIndex < imageSrc2.length - 1) {
      const newIndex = resultIndex + 1;
      setResultIndex(newIndex);
      setResultImage(imageSrc2[newIndex]);
    }
  };

  const prevResultImage = () => {
    if (resultIndex > 0) {
      const newIndex = resultIndex - 1;
      setResultIndex(newIndex);
      setResultImage(imageSrc2[newIndex]);
    }
  };

  return (
    <Row gutter={24}>
      <Col span={12}>
        <div style={{ height: 'calc(100vh - 120px)', overflow: 'auto', background: theme.palette.bole1 }}>
          <div>
            <Select value={selectedFolder} onChange={setSelectedFolder} style={{ width: '100%' }}>
              {folders.map(folder => (
                <Option key={folder} value={folder}>
                  {folder}
                </Option>
              ))}
            </Select>
            <Button onClick={prevImage}>Previous</Button>
            <Button onClick={nextImage}>Next</Button>
            <select onChange={e => setCurrentImage(e.target.value)} value={currentImage}>
              {imageSrc.map(image => (
                <option key={image} value={image}>
                  {image}
                </option>
              ))}
            </select>
          </div>
          {currentImage && (
            <img src={`http://localhost:5000/image/${currentImage}`} alt='Current Image' width='600' />
          )}
        </div>
      </Col>
      <Col span={12}>
        <div style={{ height: 'calc(100vh - 120px)', overflow: 'auto', background: theme.palette.bole1 }}>
          <div>
            <Select value={selectedResultFolder} onChange={setSelectedResultFolder} style={{ width: '100%' }}>
              {resultFolders.map(folder => (
                <Option key={folder} value={folder}>
                  {folder}
                </Option>
              ))}
            </Select>
            <Button onClick={prevResultImage}>Previous</Button>
            <Button onClick={nextResultImage}>Next</Button>
            <select onChange={e => setResultImage(e.target.value)} value={resultImage}>
              {imageSrc2.map(image => (
                <option key={image} value={image}>
                  {image}
                </option>
              ))}
            </select>
            <Button onClick={runAIModel}>Run AI Model</Button>
          </div>
          {resultImage && (
            <img src={`http://localhost:5000/result2/${resultImage}`} alt='Result Image' width='600' />
          )}
        </div>
      </Col>
    </Row>
  );
}
