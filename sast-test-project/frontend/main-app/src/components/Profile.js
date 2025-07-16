import React from 'react';

function Profile({ userInput }) {
  // УЯЗВИМОСТЬ: XSS через dangerouslySetInnerHTML
  return (
    <div>
      <h1>User Profile</h1>
      <div dangerouslySetInnerHTML={{ __html: userInput }} />
    </div>
  );
}

export default Profile;