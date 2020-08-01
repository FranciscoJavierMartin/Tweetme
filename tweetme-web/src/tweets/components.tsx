import React from 'react';
import { useEffect } from 'react';
import { useState } from 'react';
import { loadTweets } from '../lookup';

export const Tweet = (props) => {
  const { tweet, className } = props;
  return (
    <div className={className}>
      <p>{tweet.content}</p>
      <ActionBtn tweet={tweet} action={{ type: 'like', display: 'Likes' }} />
      <ActionBtn
        tweet={tweet}
        action={{ type: 'unlike', display: 'Unlikes' }}
      />
      <ActionBtn
        tweet={tweet}
        action={{ type: 'retweet', display: 'Retweet' }}
      />
    </div>
  );
};

export const ActionBtn = (props) => {
  const { tweet, className, action } = props;
  const actionDisplay = action.display ? action.display : 'Action';
  let likes = tweet.likes;
  const handleClick = (event) => {
    event.preventDefault();
    if (action.type === 'like') {
      console.log(likes + 1);
      likes = tweet + 1;
    }
  };
  const display =
    action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay;
  return <button className={className}>{display}</button>;
};

export const TweetsList = (props) => {
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
  );
};
