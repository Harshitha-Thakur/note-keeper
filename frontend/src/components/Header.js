// src/components/Header.js
import React from 'react';
import { Link } from 'react-router-dom';

const Header = ({ user }) => {
  return (
      <header>
          <nav>
              <Link to="/">Home</Link>
              {user ? (
                  <span>Welcome, {user.username}</span>
              ) : (
                  <>
                      <Link to="/login">Login</Link>
                      <Link to="/register">Register</Link>
                  </>
              )}
          </nav>
      </header>
  );
};

export default Header;