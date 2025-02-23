import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import Chat from './Chat.jsx';

createRoot(document.getElementById('root')).render(
  //<StrictMode>
    <Router>
      <Routes>

        <Route path="/count" element={<App />} />
        
        <Route path="/" element={<Chat />} />

      </Routes>
    </Router>
  //</StrictMode>, 
);
