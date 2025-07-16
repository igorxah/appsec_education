import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import Profile from './components/Profile';
import CommentForm from './components/CommentForm';

function App() {
  const [userInput, setUserInput] = useState('');

  return (
    <Router>
      <div>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/profile">Profile</Link>
        </nav>

        <Route path="/profile">
          <Profile userInput={userInput} />
        </Route>
        
        <Route exact path="/">
          <CommentForm setUserInput={setUserInput} />
        </Route>
      </div>
    </Router>
  );
}

export default App;