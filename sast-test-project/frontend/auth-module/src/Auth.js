import React, { useState } from 'react';
import axios from 'axios';

function Auth() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    // УЯЗВИМОСТЬ: Пароль в plaintext
    axios.post('http://localhost:5001/login', { username, password })
      .then(response => {
        localStorage.setItem('token', response.data.token);  // УЯЗВИМОСТЬ: XSS через localStorage
      })
      .catch(error => console.error(error));
  };

  return (
    <div>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Auth;