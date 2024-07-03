import react, { useEffect, useState } from 'react';
import axios from 'axios';

export default function ImagePage() {
  const [imageSrc, setImageSrc] = useState([]);
  const [currentImage, setCurrentImage] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);

  // this show result image
  const [imageSrc2, setImageSrc2] = useState([]);
  const [resultImage, setResultImage] = useState('');
  const [resultIndex, setResultIndex] = useState(0);

  useEffect(() => {
    getImageData();
  }, []);

  function getImageData() {
    axios
      .get('http://localhost:5000/images') // , { responseType: 'blob' }
      .then((response) => {
        console.log(response.data);
        setImageSrc(response.data);
        if (response.data.length > 0) {
          setCurrentImage(response.data[0]);
          //   setCurrentIndex(0);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }

  // function getResultImage() {
  //   axios.get()

  const nextImage = () => {
    const newIndex = currentIndex + 1;
    setCurrentIndex(newIndex);
    setCurrentImage(imageSrc[newIndex]);
  };

  const prevImage = () => {
    const newIndex = currentIndex - 1;
    setCurrentIndex(newIndex);
    setCurrentImage(imageSrc[newIndex]);
  };

  const handleImageChange = (event) => {
    const changingImage = event.target.value; // files[0]
    const newIndex = imageSrc.indexOf(changingImage);
    setCurrentIndex(newIndex);
    setCurrentImage(changingImage);
  };

  //   const deleteImage = () => {
  //     axios
  //       .delete('http://localhost:5000/image')
  //       .then((response) => {
  //         console.log(response.data);
  //         setImageSrc([]);
  //         setCurrentImage(0);
  //         setCurrentIndex(0);
  //       })
  //       .catch((error) => {
  //         console.log(error);
  //       });
  //   }

  return (
    <div style={{ height: 'calc(100vh - 120px)', overflow: 'auto' }}>
      <div>
        <button onClick={prevImage}>Previous</button>
        <button onClick={nextImage}>Next</button>
        <select onChange={handleImageChange} value={currentImage}>
          {imageSrc.map((image) => (
            <option key={image} value={image}>
              {image}
            </option>
          ))}
        </select>
      </div>
      <div style={{ width: '50%', float: 'left', position: 'relative' }}>
        {currentImage && (
          <img
            src={`http://localhost:5000/image/${currentImage}`}
            alt='Current Image'
            width='600'
          />
        )}
      </div>

      <div style={{ width: '50%', float: 'right', position: 'relative' }}>
        <div>
          <button onClick={prevImage}>Previous</button>
          <button onClick={nextImage}>Next</button>
          <select onChange={handleImageChange} value={currentImage}>
            {imageSrc.map((image) => (
              <option key={image} value={image}>
                {image}
              </option>
            ))}
          </select>
        </div>
        <div>
          <img
            src={`http://localhost:5000/image/${currentImage}`}
            alt='Current Image'
            width='600'
          />
        </div>
      </div>
    </div>
  );
}
