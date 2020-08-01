import React from 'react';
import { useEffect } from 'react';
import { useState } from 'react';
import { loadTweets } from '../lookup';

export const Tweet = (props) => {
  const { tweet, className } = props;
  return (
    <div className={className}>
      <p>{tweet.content}</p>
      <ActionBtn tweet={tweet} action={{ type: 'like' }} />
    </div>
  );
};

export const ActionBtn = (props) => {
  const { tweet, className, action } = props;
  return action.type === 'like' ? (
    <button className={className}>{tweet.likes} Likes</button>
  ) : null;
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
