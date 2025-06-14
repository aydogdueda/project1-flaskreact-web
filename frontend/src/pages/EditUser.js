import axios from "axios";
import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

export default function EditUser(){

    const navigate = useNavigate();

    const [inputs, setInputs] = useState({});

    const {id} = useParams();

    useEffect(() => {
        getUser();
    }, []);

    function getUser(){
        axios.get('https://react-web-dugta7gmcab0dhab.canadacentral-01.azurewebsites.net/userdetails/${id}').then(function(response){
            console.log(response.data);
            setInputs(response.data);
        });
    }

    const handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(prevInputs => ({ ...prevInputs, [name]: value }));
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        axios.put(`http://react-web-dugta7gmcab0dhab.canadacentral-01.azurewebsites.net/userupdate/${id}`, inputs).then(function(response){
            console.log(response.data);
            navigate('/');
        });
    }

    return (
        <div>
            <div className="container h-100">
            <div className="row">
                <div className="col-2"></div>
                <div className="col-8">
                <h1>Edit user</h1>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label>Name</label>
                        <input type="text" value={inputs.name} className="form-control" name="name" onChange={handleChange} />
                    </div>
                    <div className="mb-3">
                        <label>Email</label>
                        <input type="text" value={inputs.email} className="form-control" name="email" onChange={handleChange} />
                    </div>
                    <button type="submit" name="update" className="btn btn-primary">Save</button>
                </form> 
                </div>
                <div className="col-2"></div>
            </div>
            </div>
        </div>
    );
}
