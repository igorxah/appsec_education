import React, { useState } from 'react';
import axios from 'axios';

function CommentForm({ setUserInput }) {
  const [comment, setComment] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // УЯЗВИМОСТЬ: Отправка необработанного пользовательского ввода
    setUserInput(comment);
    
    // УЯЗВИМОСТЬ: CSRF - нет токена
    axios.post('http://localhost:5000/api/comments', { comment })
      .then(response => console.log(response))
      .catch(error => console.error(error));
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea 
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        placeholder="Enter your comment"
      />
      <button type="submit">Submit</button>
    </form>
  );
}

export default CommentForm;