import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import NoteEditor from './components/NoteEditor';
import NoteList from './components/NoteList';
import Login from './components/Login';
import Register from './components/Register';
import UserProfile from './components/UserProfile';
import SyncManager from './components/SyncManager';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:5000'

const App = () => {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [user, setUser] = useState(null);

    useEffect(() => {
        if (token) {
            axios.get('/api/auth/profile', {
                headers: { Authorization: `Bearer ${token}` }
            }).then(response => {
                setUser(response.data);
            }).catch(error => {
                console.error('Error fetching user profile:', error);
            });
        }
    }, [token]);

    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<NoteList />} />
                <Route path="/edit/:id" element={<NoteEditor />} />
                <Route path="/login" element={<Login setToken={setToken} />} />
                <Route path="/register" element={<Register />} />
                <Route path="/profile" element={<UserProfile user={user} />} />
                <Route path="/sync" element={<SyncManager />} />
            </Routes>
            <Footer />
        </Router>
    );
};

export default App;