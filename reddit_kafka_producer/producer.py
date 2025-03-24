import praw
import json
import os
import time
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from dotenv import load_dotenv

print('Start')

def configure():
    load_dotenv()

configure()



# Create Kafka topic if it doesn't exist
def create_topic(topic_name, bootstrap_servers):
    print(bootstrap_servers)
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    existing_topics = admin_client.list_topics()
    
    if topic_name in existing_topics:
        print(f"Topic '{topic_name}' already exists.")
    else:
        new_topic = NewTopic(name=topic_name, num_partitions=3, replication_factor=1)
        admin_client.create_topics([new_topic])
        print(f"Topic '{topic_name}' created successfully.")

# Reddit API credentials from environment variables
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

# Kafka producer setup
topic_name = 'reddit'
bootstrap_servers = 'localhost:9092'
# print(bootstrap_servers)
create_topic(topic_name, bootstrap_servers)

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',
    retries=5
)

# Define the subreddit and start streaming submissions
subreddit = reddit.subreddit("sports")

def stream_reddit_comments():
  while True:
        try:
            for comment in subreddit.stream.comments():  # Removed skip_existing for better reliability
                message = {'comment': comment.body}
                producer.send(topic_name, value=message)
                print(f"Produced: {message}")
                time.sleep(0.5)
        except Exception as e:
            print(f"Error: {e}. Retrying in 10 seconds...")
            time.sleep(10)  # Retry with dela  
stream_reddit_comments()

    
