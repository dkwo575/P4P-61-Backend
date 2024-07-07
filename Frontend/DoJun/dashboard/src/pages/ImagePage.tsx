import react, { useEffect, useState } from 'react';
import axios from 'axios';
import { set } from 'lodash-es';
import { Col, Row, Typography, Button, DatePicker, Select } from 'antd';
import { SVGElementPropKeys } from 'recharts/types/util/types';
import theme from '../theme';
import ImageArea from '../components/ImageArea.tsx';

const { Option } = Select;

export default function ImagePage() {
  return (
    <Col span={24}>
      <Row>
        <Col span={24}>
          <ImageArea />
        </Col>
      </Row>
    </Col>
  );

  // const [imageSrc, setImageSrc] = useState([]);
  // const [currentImage, setCurrentImage] = useState('');
  // const [currentIndex, setCurrentIndex] = useState(0);

  // // this show result image
  // const [imageSrc2, setImageSrc2] = useState([]);
  // const [resultImage, setResultImage] = useState('');
  // const [resultIndex, setResultIndex] = useState(0);

  // useEffect(() => {
  //   getImageData();
  // }, []);

  // useEffect(() => {
  //   getResultImage();
  // }, []);

  // function getImageData() {
  //   axios
  //     .get('http://localhost:5000/images') // , { responseType: 'blob' }
  //     .then((response) => {
  //       console.log(response.data);
  //       setImageSrc(response.data);
  //       if (response.data.length > 0) {
  //         setCurrentImage(response.data[0]);
  //         //   setCurrentIndex(0);
  //       }
  //     })
  //     .catch((error) => {
  //       console.log(error);
  //     });
  // }

  // function getResultImage() {
  //   axios
  //     .get('http://localhost:5000/result')
  //     .then((response) => {
  //       console.log(response.data);
  //       setImageSrc2(response.data);
  //       if (response.data.length > 0) {
  //         setResultImage(response.data[0]);
  //         //   setCurrentIndex(0);
  //       }
  //     })
  //     .catch((error) => {
  //       console.log(error);
  //     });
  // }

  // // function getResultImage() {
  // //   axios.get()

  // const nextImage = () => {
  //   const newIndex = currentIndex + 1;
  //   setCurrentIndex(newIndex);
  //   setCurrentImage(imageSrc[newIndex]);
  // };

  // const prevImage = () => {
  //   const newIndex = currentIndex - 1;
  //   setCurrentIndex(newIndex);
  //   setCurrentImage(imageSrc[newIndex]);
  // };

  // const handleImageChange = (event) => {
  //   const changingImage = event.target.value; // files[0]
  //   const newIndex = imageSrc.indexOf(changingImage);
  //   setCurrentIndex(newIndex);
  //   setCurrentImage(changingImage);
  // };

  // const nextResultImage = () => {
  //   const newIndex = resultIndex + 1;
  //   setResultIndex(newIndex);
  //   setResultImage(imageSrc2[newIndex]);
  // };

  // const prevResultImage = () => {
  //   const newIndex = resultIndex - 1;
  //   setResultIndex(newIndex);
  //   setResultImage(imageSrc2[newIndex]);
  // };

  // const handleResultChange = (event) => {
  //   const changingImage = event.target.value; // files[0]
  //   const newIndex = imageSrc2.indexOf(changingImage);
  //   setResultIndex(newIndex);
  //   setResultImage(changingImage);
  // };

  // //   const deleteImage = () => {
  // //     axios
  // //       .delete('http://localhost:5000/image')
  // //       .then((response) => {
  // //         console.log(response.data);
  // //         setImageSrc([]);
  // //         setCurrentImage(0);
  // //         setCurrentIndex(0);
  // //       })
  // //       .catch((error) => {
  // //         console.log(error);
  // //       });
  // //   }

  // return (
  //   <>
  //     <Row>
  //       <Col span={24}>
  //         <div
  //           style={{
  //             height: 'calc(100vh - 120px)',
  //             overflow: 'auto',
  //             background: theme.palette.bole1,
  //           }}
  //         >
  //           <div>
  //             <div>
  //               <Button onClick={prevImage}>Previous</Button>
  //               <Button onClick={nextImage}>Next</Button>
  //               <select onChange={handleImageChange} value={currentImage}>
  //                 {imageSrc.map((image) => (
  //                   <option key={image} value={image}>
  //                     {image}
  //                   </option>
  //                 ))}
  //               </select>
  //             </div>
  //             <div style={{ width: '50%', float: 'left', position: 'relative' }}>
  //               {currentImage && (
  //                 <img
  //                   src={`http://localhost:5000/image/${currentImage}`}
  //                   alt='Current Image'
  //                   width='600'
  //                 />
  //               )}
  //             </div>
  //           </div>
  //           <div style={{ width: '50%', float: 'right', position: 'relative' }}>
  //             <div>
  //               <Button onClick={prevResultImage}>Previous</Button>
  //               <Button onClick={nextResultImage}>Next</Button>
  //               <select onChange={handleResultChange} value={resultImage}>
  //                 {imageSrc2.map((image) => (
  //                   <option key={image} value={image}>
  //                     {image}
  //                   </option>
  //                 ))}
  //               </select>
  //             </div>
  //             <div>
  //               <img
  //                 src={`http://localhost:5000/result2/${resultImage}`}
  //                 alt='Result Image'
  //                 width='600'
  //               />
  //             </div>
  //           </div>
  //         </div>
  //       </Col>
  //     </Row>
  //   </>
  // );
}
