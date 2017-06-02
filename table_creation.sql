CREATE TABLE public.tweets
(
  id integer NOT NULL,
  handle character varying NOT NULL,
  is_retweeted boolean NOT NULL,
  original_author character varying,
  text text NOT NULL,
  favorite_count integer NOT NULL,
  retweet_count integer NOT NULL,
  "time" timestamp without time zone NOT NULL,
  CONSTRAINT "Tweets_pkey" PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.tweets
  OWNER TO student;
  
 CREATE TABLE public.hashtag
(
  name character varying NOT NULL,
  CONSTRAINT "Hashtags_pkey" PRIMARY KEY (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.hashtag
  OWNER TO student;
  
  CREATE TABLE public.tweets_hashtag
(
  tweet_id integer NOT NULL,
  hashtag_name character varying NOT NULL,
  CONSTRAINT "Tweets_Hashtag_pkey" PRIMARY KEY (tweet_id, hashtag_name),
  CONSTRAINT "Tweets_Hashtag_Hashtag_name_fkey" FOREIGN KEY (hashtag_name)
      REFERENCES public.hashtag (name) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "Tweets_Hashtag_Tweet_ID_fkey" FOREIGN KEY (tweet_id)
      REFERENCES public.tweets (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.tweets_hashtag
  OWNER TO student;
  
  CREATE TABLE public.hashtag_hashtag
(
  name1 character varying NOT NULL,
  name2 character varying NOT NULL,
  tweet_id integer NOT NULL,
  CONSTRAINT hashtag_hashtag_pkey PRIMARY KEY (tweet_id, name1, name2),
  CONSTRAINT "Hashtag_Hashtag_name1_fkey" FOREIGN KEY (name1)
      REFERENCES public.hashtag (name) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "Hashtag_Hashtag_name2_fkey" FOREIGN KEY (name2)
      REFERENCES public.hashtag (name) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.hashtag_hashtag
  OWNER TO student;