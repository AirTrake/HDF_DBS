
#import the csv libary
import csv
#initialisig global variables
Tweet_ID=0
Hashtag_List=set()

#Function to filter the hashtags out of a given text and also making the text so that postgres can read it.
def text_filter(strings):
	i = 0
	hashtags = []
	strng = ''
	while i < len(strings):
		#filter by the first char of the string to determinate if it's a hashtag
		if strings[i] == '#':
			tag=strings[i]
			a=i
			strng+=strings[i]
			i+=1
			#figuring out the lenght of the hashtag
			while strings[i].isalpha() or strings[i].isdigit():
				tag+=strings[i]
				strng+=strings[i]
				#making sure not to get an out of bounds error
				if (i<(len(strings)-1)):
					i+=1
				else:
					break
			hashtags.append(tag)
		#we found no other solution to mask the "'"  charakter so we had to remove it :(
		elif strings[i] != "'":		
			strng+=strings[i]
		i+=1
	return [strng, hashtags]

#converts the rows of data into an Array of ditionarys representing the tables in the Database
def process_row(row):
	global Tweet_ID
	global Hashtag_List
	Tweets = row.copy()
	Tweets.update({"ID" : (str)(Tweet_ID)})
	#delete the unused columns
	del Tweets["in_reply_to_screen_name"]
	del Tweets["source_url"]
	del Tweets["truncated"]
	del Tweets["is_quote_status"]
	#print(Tweets)
	[text, hashtags] = text_filter(row["text"])
	Tweets.update({"text" : text})
	tags=[]
	t_h=[]
	for hashtag in hashtags:
		if not (hashtag in Hashtag_List):
			tags.append({"name" : hashtag})
			Hashtag_List.add(hashtag)
		if not (({"name" : hashtag, "tweet_ID" : (str)(Tweet_ID)}) in t_h):
			t_h.append({"name" : hashtag, "tweet_ID" : (str)(Tweet_ID) })
	pairs=[]
	#removes all duplicates to avoid SQL errors
	temp=set(hashtags)
	htags=list(temp)
	if len(htags) > 1:
		pairs = hs_pair(hashtags)
	Tweet_ID=Tweet_ID+1
	return [Tweets]+tags+t_h+pairs
	
#gets the hashtags that are in a certain row and exports a list of all the pais of this hashtags 
def hs_pair(htags):
	global Tweet_ID
	length = len(htags)
	length = len(htags)
	if length>2:
		pairs=[]
		for i in range(length):
			#makes sure not to pair with itself
			if(i!=0):
				pairs.append({"tweet_ID": (str)(Tweet_ID), "name1": htags[0], "name2": htags[i]})
		return pairs+hs_pair(htags[1:])
	else:
		return [{"tweet_ID": (str)(Tweet_ID), "name1": htags[0], "name2": htags[1]}]

#gets al list of ditionarys and turn these into SQL code 
def do_textdoc(help):
	endprint = ''	
	for dictionary in help:
		#from the number of entrys whitin a dictionary we can evaluate the table it belongs to
		if(len(dictionary) == 8):
			tweet = ''
			tweet += 'INSERT INTO tweets(ID, handle, text, original_author, is_retweeted, favorite_count, retweet_count, time)\n'
			tweet += 'VALUES('
			tweet += dictionary['ID'] + ", '" + dictionary['handle']+ "', '" + dictionary['text']+ "', " + clean(dictionary['original_author']) + ", '" + dictionary['is_retweet'] + "', '" + dictionary['favorite_count'] + "', '" + dictionary['retweet_count'] + "', '" + dictionary['time']+"');\n"
			endprint += tweet + '\n'
		elif(len(dictionary) == 1):
			hashtag = ''
			hashtag += 'INSERT INTO hashtag(name)\n'
			hashtag += 'VALUES('
			hashtag += "'"+ dictionary['name'] + "');\n"
			endprint += hashtag + '\n'
			print(dictionary['name'])
		elif(len(dictionary) == 2):
			t_h = ''
			t_h += 'INSERT INTO tweets_hashtag(tweet_ID, hashtag_name)\n'
			t_h += 'VALUES ('
			t_h += dictionary['tweet_ID'] + ", '" + dictionary['name'] + "');\n"
			endprint += t_h + '\n'
		else:
			h_h = ''
			h_h += 'INSERT INTO hashtag_hashtag(tweet_ID, name1, name2)\n'
			h_h += 'VALUES('
			h_h += dictionary['tweet_ID']+", '"+dictionary['name1']+"', '"+dictionary['name2'] + "');\n"
			endprint += h_h + '\n'
		#endprint returns the whole insert code for sql
	return endprint
	
#function to convert an empty string into a null value	
def clean(str):
	if str=='':
		return "null"
	else:
		return "'"+str+"'"
	
#function to write the Code in an SQL file		
def export_data(dict):	
	input = do_textdoc(dict)
	with open("data.sql", "a") as myfile:
		myfile.write(input)
		myfile.close()
		
#clears the data.sql file 		
with open("data.sql", "w") as myfile:
	myfile.close()	
		
with open("american-election-tweets.csv", "r") as f:
	reader = csv.DictReader(f, delimiter=";", dialect="excel")	
	for row in reader:
		export_data(process_row(row))


