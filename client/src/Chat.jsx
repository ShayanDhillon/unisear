import React, { useEffect, useState } from 'react'
import axios from 'axios';

const Chat = () => {
    const [UniNames, setUniNames] = useState([]);
    const [selectedUni, setSelectedUni] = useState('');
    const [message, setMessage] = useState('');

    const [loading, setLoading] = useState(true);

    //console.log("meow")

    useEffect( () => {
        const api = "http://localhost:4000/api/getInstiutionList";
        console.log("api ran")
        
        const fetchData = async() => {
            try{
                const res = await axios.get(api);
                setUniNames(['Select a University']);
                setUniNames((prevUniNames) => [...prevUniNames, ...res.data.sort()]);
                setLoading(false);
            } catch (e){
                console.error(e);
                setLoading(true);
            }
        };

        fetchData();

    }, [])

    const handleSend = async () => {
        console.log(`Selected University: ${selectedUni}`);
        console.log(`Message: ${message}`);

        const requestBody = {
          instituion: selectedUni,
          prompt: message,
        }
        const api = "http://localhost:4000/api/queryAI";
        
        const res = await axios.post(api, requestBody);
        console.log(res.data);

        // Add your send logic here
        alert(`Message to ${selectedUni}: "${message}"`);
    };

    if (loading) return <div>Loading...</div>;

    return (
    <div>
      {/* Dropdown (Select box) */}
      <select value={selectedUni} onChange={(e) => setSelectedUni(e.target.value)}>
        {UniNames.map((uni) => (
          <option key={uni} value={uni}>
            {uni}
          </option>
        ))}
      </select>

      {/* TextBox for entering the message */}
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message"
        style={{ marginLeft: '10px', padding: '5px' }}
      />

      {/* Send button */}
      <button onClick={handleSend} style={{ marginLeft: '10px', padding: '5px' }}>
        Send
      </button>
    </div>
  );
}

export default Chat
