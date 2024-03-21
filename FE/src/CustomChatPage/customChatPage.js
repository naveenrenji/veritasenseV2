import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './UploadAndListPage.css'; // Assuming you have a CSS file for styling

const UploadAndListPage = () => {
  const [files, setFiles] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const navigate = useNavigate();
  const apiUrl = process.env.REACT_APP_API_ENDPOINT;

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await axios.get(`${apiUrl}/files`);
      setFiles(response.data);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  const handleUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    setIsProcessing(true); // Show processing overlay

    try {
      await axios.post(`${apiUrl}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });

      fetchFiles(); // Refresh the file list
      setIsProcessing(false); // Hide processing overlay
    } catch (error) {
      console.error('Upload failed:', error);
      setIsProcessing(false); // Hide processing overlay in case of error
      alert('Upload failed. Please try again.');
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleUpload(file);
    }
  };

  const handleFileClick = async (filename) => {
    try {
        const response = await axios.get(`${apiUrl}/chatbot/${filename}`);
        navigate("/chatbot")
    }  
    catch (error) {
        console.error('Upload failed:', error);
        setIsProcessing(false); // Hide processing overlay in case of error
        alert('Upload failed. Please try again.');
      }
    navigate(`/chatbot`);
  };

  return (
    <div className="container">
      <div className="upload-section">
        <h2>Upload File</h2>
        <input type="file" onChange={handleFileChange} accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" />
      </div>
      <div className="file-list-section">
        <h2>Chatbot List</h2>
        <table>
          <thead>
            <tr>
              <th>Index</th>
              <th>File Names</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file, index) => (
              <tr key={index} className="clickable-row" onClick={() => handleFileClick(file)}>
                <td>{index + 1}</td>
                <td>{file}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {isProcessing && (
        <div className="processing-overlay">
          Processing file... Please wait.
        </div>
      )}
    </div>
  );
};

export default UploadAndListPage;
