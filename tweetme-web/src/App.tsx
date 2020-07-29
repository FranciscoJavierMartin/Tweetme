import React, { useState, useEffect } from 'react';

function loadTweets(callback: any) {
  const xhr = new XMLHttpRequest();
  const method = 'GET';
  const url = 'http://localhost:8000/api/tweets';
  const responseType = 'json';

  xhr.responseType = responseType;
  xhr.open(method, url);
  xhr.onload = function () {
    callback(xhr.response, xhr.status);
  };
  xhr.onerror = () => {
    callback({ message: 'The request was an error' }, 400);
  };
  xhr.send();
}

const App = () => {
  const [tweets, setTweets] = useState<any[]>([]);

  useEffect(() => {
    loadTweets((response: any[], status) => {
      if (status === 200) {
        setTweets(response);
      }
    });
  }, []);

  return (
    <div>
      <div>
        {tweets.map((tweet) => {
          return (
            <Tweet
              tweet={tweet}
              key={tweet.id}
              className='my-5 py-5 border bg-white text-dark'
            />
          );
        })}
      </div>
    </div>
  );
};

const Tweet = (props) => {
  const { tweet, className } = props;
  return (
    <div className={className}>
      <p>{tweet.content}</p>
    </div>
  );
};
export default App;
