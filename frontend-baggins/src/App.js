import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import MainPage from "./pages/mainPage";
import AnalisPage from './pages/analisPage';
import UsersPage from './pages/usersPage';
import OneUserPage from './pages/oneUserPage';
import Example from './pages/aaaaaaaaaaaaaaaaaaaaa';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<MainPage />}></Route>
        <Route path='/a' element={<Example />}></Route>
        <Route path='/analis' element={<AnalisPage />}></Route>
        <Route path='/users' element={<UsersPage />}></Route>
        <Route path='/oneuser' element={<OneUserPage />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
