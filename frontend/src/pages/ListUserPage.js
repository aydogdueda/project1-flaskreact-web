import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from 'react-router-dom';

export default function ListUserPage() {
    
    const [users, setUsers] = useState([]);
    useEffect(() => {
        getUsers();
    }, []);

    function getUsers() {
        axios.get('https://react-web-dugta7gmcab0dhab.canadacentral-01.azurewebsites.net/listusers')
            .then(function (response) {
                console.log(response.data);
                setUsers(response.data);
            })
            .catch(function (error) {
                console.error("Veri alınamadı:", error);
            });
    }
    const deleteUser = (id) => {
        axios.delete(`http://react-web-dugta7gmcab0dhab.canadacentral-01.azurewebsites.net/userdelete/${id}`).then(function(response){
            console.log(response.data);
            getUsers();
        });
        alert("Successfully Deleted");
    }


    return (
        <div>
            <div className="container h-100">
                <div className="row h-100">
                    <div className="col-12">
                        <p>
                            <Link to="/addnewuser" className="btn btn-success">Add New User</Link>
                        </p>
                        <h1>List Users</h1>
                        <table className="table table-bordered table-striped">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Date Added</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map((user, key) => (
                                    <tr key={key}>
                                        <td>{user.id}</td>
                                        <td>{user.name}</td>
                                        <td>{user.email}</td>
                                        <td>{new Date(user.date).toLocaleString()}</td>
                                        <td>
                                            <Link to ={`user/${user.id}/edit`} className="btn btn-success" style={{marginRight: "10px"}}>Edit</Link>
                                            <button onClick={() => deleteUser(user.id)} className="btn btn-sm btn-danger">Delete</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}
