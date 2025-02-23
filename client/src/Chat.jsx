import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Chat = () => {
  const [uniNames, setUniNames] = useState(['Select a University']);
  const [selectedUni, setSelectedUni] = useState('');
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);  // Added state for messages
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    setUniNames([]);
    const api = "http://localhost:4000/api/getInstiutionList";

    
    const fetchData = async () => {
        try {
            const res = await axios.get(api);
            setUniNames(['Select A University']);
            setUniNames((p) => [...p, ...res.data.sort()]);

            setLoading(false);
        } catch (e) {
            console.error(e);
            setLoading(true);
        }
    };

    fetchData();
  }, [])


  useEffect(() =>{
    if(!selectedUni){
      setMessages([]);
    }
  }, [selectedUni])


  const handleSend = () => {
    if (message.trim()) {
      setMessages((prevMessages) => [...prevMessages, message]);  // Add new message to messages state
      setMessage('');  // Clear input box after entry
      //console.log(messages);

      // call backend
      const api = "http://localhost:4000/api/queryAI";
      
      const callQuery = async () => {
        const res = await axios.post(api, requestBody);
        console.log(res.data);

      }

      callQuery();

    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {  // Check if Enter (Return) key was pressed
      handleSend();
    }
  };

  if (loading) return <div>Loading...</div>;


  return (
    <div className="flex h-screen bg-yellow-100 p-4">
      {selectedUni ? (
        <SearchPage 
          university={selectedUni} 
          message={message} 
          setMessage={setMessage} 
          setSelectedUni={setSelectedUni} // Pass the function
          handleSend={handleSend}
          handleKeyPress={handleKeyPress} // Pass handleKeyPress to SearchPage
          messages={messages} // Pass messages to SearchPage
        />
      ) : (
        <HomePage uniNames={uniNames} setSelectedUni={setSelectedUni} />
      )}
      
      {/* Add the Google Fonts import here */}
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600&family=Jaro:wght@400;600&display=swap');

          /* Apply the fonts */
          body, input, select, h1, h2 {
            font-family: 'Instrument Sans', sans-serif;
          }

          h1, h2 {
            font-family: 'Jaro', sans-serif;
          }
        `}
      </style>
    </div>
  );
};

const HomePage = ({ uniNames, setSelectedUni }) => {
  return (
    <div className="flex flex-col items-center justify-center w-full bg-white p-8 shadow-lg rounded-lg">
      <h1 className="flex" style={{ position: 'absolute', top: '-0.8em', left: '0.2em' }}>
        Unisear
        <img src="/Unisear_Logo.png" alt="Logo" style={{ height: '1.2em', width: '1.2em', transform: 'translate(0.1em, 0.2em)' }} />
      </h1>
      <p style={{ textAlign: 'center', marginTop: '0.5rem', fontSize: '2rem' }}>
        Welcome to <strong style={{ fontFamily: 'Jaro' }}>Unisear!</strong> The easy way to find the information you need about any <i>Canadian </i>
        university, saving you time from searching multiple websites.
      </p>
      <p style={{ textAlign: 'center', marginTop: '1rem', fontSize: '1.5rem' }}>To get started, select a university below.</p>
      <select
  style={{
    marginTop: '1rem',
    padding: '0.5rem',
    border: '1px solid #E1CACA',
    borderRadius: '0.25rem',
    backgroundColor: '#463D3D',
    color: '#ffffff',
    width: '20rem', // Adjust width as needed
    appearance: 'none',
    overflowY: 'auto', // Allow scrolling
  }}
  onChange={(e) => e.target.value !== 'Select a University' && setSelectedUni(e.target.value)}
  size="1" // Keeps the box size fixed when closed
  onFocus={(e) => e.target.size = 8} // Expand dropdown to show 8 options at once
  onBlur={(e) => e.target.size = 1} // Collapse dropdown when not focused
>
  {uniNames.map((uni) => (
    <option key={uni} value={uni} style={{ backgroundColor: '#463D3D', color: '#ffffff' }}>
      {uni}
    </option>
  ))}
</select>
    </div>
  );
};

const SearchPage = ({ university, message, setMessage, setSelectedUni, handleSend, handleKeyPress, messages }) => {
  return (
    <div className="flex flex-col w-full bg-white p-8 shadow-lg rounded-lg relative">
      <h1 
        className="flex cursor-pointer transition-colors duration-300" 
        style={{ 
          position: 'absolute', 
          top: '-0.8em', 
          left: '0.2em',
          color: 'inherit', // Keep original text color
        }} 
        onClick={() => setSelectedUni('')}
        onMouseEnter={(e) => e.target.style.color = '#97655d'}
        onMouseLeave={(e) => e.target.style.color = ''} // Reset to default
      >
        Unisear
        <img 
          src="/Unisear_Logo.png" 
          alt="Logo" 
          style={{ height: '1.2em', width: '1.2em', transform: 'translate(0.1em, 0.2em)' }} 
        />
      </h1>
      <h2 className="text-xl mt-4">{university}</h2>

      {/* This is the large box for messages */}
      <div
        style={{
          width: '50em', 
          height: '45em', 
          backgroundColor: '#978b8b', 
          borderRadius: '10px', 
          padding: '1rem',
          marginBottom: '1rem',
          border: '2px solid #6c6464',
          overflowY: 'auto', // Allow scrolling if messages exceed box height
        }}
      >
        {/* Displaying messages as chat bubbles inside the large box */}
        <div style={{ padding: '1rem' }}>
          {messages.map((msg, index) => (
            <div 
              key={index} 
              style={{
                backgroundColor: '#a83319',
                padding: '0.5rem',
                borderRadius: '10px',
                marginBottom: '0.5rem',
                textAlign: 'left',
                maxWidth: '80%',
                marginLeft: 'auto',
                marginRight: 'auto',
                fontWeight: 'bold',  // Make the text bold
              }}
            >
              {msg}
            </div>
          ))}
        </div>
      </div>

      <div className="flex items-center bg-gray-200 rounded-lg p-3 mt-4">
        <style>
          {`
            input::placeholder {
              color: #ad9f9f;
              opacity: 1;
            }
          `}
        </style>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyPress}  // Add keydown event to capture Enter key
          placeholder="What do you want to know?"
          style={{
            border: "1px solid #ad9f9f",
            outline: "1px solid #ad9f9f",
            backgroundColor: "#ddcbca",
            borderRadius: "10px",
            padding: "0.5rem",
            width: "90%",
            color: "#1c1c1c"
          }}
        />
        
        <img 
          src="/Unisear_MG.png" 
          alt="Search" 
          style={{ height: '1.5em', width: '1.5em', transform: 'translate(0.4em, 0.6em)', cursor: 'pointer' }} 
          onClick={handleSend} 
        />
      </div>
    </div>
  );
};

export default Chat;