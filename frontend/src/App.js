import React, { } from 'react';
import './App.css';

import { BrowserRouter, Routes, Route } from 'react-router-dom';

import ListUserPage from "./pages/ListUserPage";
import CreateUser from './pages/CreateUser';
import EditUser from './pages/EditUser';

function App() {
  return (
    <div className="vh-100 gradient-costum">
    <div className="container">
      <h1 className= "page-header text-center">React-JS and Python Flask CRUD Create, Read, Update and Delete MySql-Database</h1>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<ListUserPage />} />
          <Route path="/addnewuser" element={<CreateUser />} />
          <Route path="user/:id/edit" element={<EditUser />} />
        </Routes>        
      </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
