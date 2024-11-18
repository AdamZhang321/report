import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import ReportResult from './components/ReportResult';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/result" element={<ReportResult />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
); 