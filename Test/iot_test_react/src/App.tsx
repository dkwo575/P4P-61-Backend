import React, { useState, useEffect } from 'react';
import axios from './utils/axios.js';

function App() {
  const [imageSrc, setImageSrc] = useState<string | null>(null);

  useEffect(() => {
    // Fetch the PNG image from the backend
    axios.get('/png', { responseType: 'arraybuffer' }) // Set responseType to 'arraybuffer' to handle binary data
        .then(response => {
          // Convert the array buffer to base64 string
          const base64String = btoa(
              new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), '')
          );
          setImageSrc(`data:image/png;base64,${base64String}`);
        })
        .catch(error => {
          console.error('Error fetching image:', error);
        });
  }, []);

  return (
      <div className="App">
        <header className="App-header">
          {imageSrc ? (
              <img src={imageSrc} alt="PNG Image" />
          ) : (
              <p>Loading...</p>
          )}
          <p>
            Edit <code>src/App.tsx</code> and save to reload.
          </p>
          <a
              className="App-link"
              href="https://reactjs.org"
              target="_blank"
              rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
  );
}

export default App;
