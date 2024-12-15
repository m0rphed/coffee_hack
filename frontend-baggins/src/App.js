import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import MainPage from "./pages/mainPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<MainPage />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
