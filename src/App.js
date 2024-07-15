// Filename: App.js

import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
    const [data, setData] = useState({
        name: "",
        age: 0,
        date: "",
        programming: "",
        imgpath: ""
    });

    const [inputValue, setInputValue] = useState("");
    const [status, setStatus] = useState("active");
    const [email, setEmail] = useState("");

    useEffect(() => {
        fetch("/data").then((res) =>
            res.json().then((data) => {
                setData({
                    name: data.Name,
                    age: data.Age,
                    date: data.Date,
                    programming: data.programming,
                    imgpath: data.imgpath
                });
            })
        );
    }, []);

    const handleChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleStatusChange = (event) => {
        setStatus(event.target.value);
    };

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        fetch('/add_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: inputValue, status, email })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>React and Flask</h1>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        value={inputValue}
                        onChange={handleChange}
                        placeholder="Enter your username"
                    />
                    <input
                        type="text"
                        value={email}
                        onChange={handleEmailChange}
                        placeholder="Enter your email"
                    />
                    <select value={status} onChange={handleStatusChange}>
                        <option value="active">Active</option>
                        <option value="inactive">Inactive</option>
                    </select>
                    <button type="submit">Submit</button>
                </form>
                <p>Input Value: {inputValue}</p>
                <p>Email: {email}</p>
                <p>Status: {status}</p>
                <p>{data.name}</p>
                <p>{data.age}</p>
                <p>{data.date}</p>
                <p>{data.programming}</p>
                <p>{data.imgpath}</p>
                <img src={data.imgpath} alt="alt text" />
            </header>
        </div>
    );
}

export default App;
