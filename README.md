
# Real-Time Reddit Data Pipeline

## ✅ Project Overview
This project builds a real-time data pipeline that streams messages from Reddit using the Reddit API, ingests the data through Apache Kafka, processes it using Apache Spark, and stores the transformed data in 
MongoDB. All components are containerized using Docker and orchestrated via Docker Compose.

---

## 📁 Folder Structure
```
.
├── docker-compose.yml      # Docker Compose file to orchestrate services
├── kafka/                  # Kafka-related setup and configuration
├── spark/                  # Spark scripts and job definitions
├── reddit/                 # Reddit API producer scripts
├── mongo/                  # MongoDB data storage setup
├── notebooks/              # Optional analysis/visualization
├── README.md               # Project documentation
```

---

## 🔧 Tools & Technologies
- **Reddit API (PRAW)** – Stream Reddit posts/comments
- **Apache Kafka** – Messaging queue for streaming data
- **Apache Spark** – Real-time stream processing
- **MongoDB** – NoSQL database for storing structured results
- **Docker & Docker Compose** – Container orchestration and deployment

---

## 🚀 Pipeline Overview

1. **Reddit Producer**
   - Uses PRAW (Python Reddit API Wrapper) to connect to Reddit.
   - Streams live posts/comments and sends messages to Kafka topic.

2. **Kafka Broker**
   - Receives messages from Reddit producer and buffers them in a topic.

3. **Spark Consumer**
   - Reads messages from Kafka in real time.
   - Applies transformations and data cleaning.

4. **MongoDB Sink**
   - Transformed data is saved into MongoDB collections.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/reddit-kafka-pipeline.git
cd reddit-kafka-pipeline
```

### 2. Set Up Reddit API Credentials
Create a `.env` file with the following:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

### 3. Launch All Services
```bash
docker-compose up --build
```

This will start:
- Kafka broker and Zookeeper
- Reddit producer
- Spark streaming job
- MongoDB database

### 4. Access MongoDB
You can access MongoDB on `localhost:27017` using MongoDB Compass or the CLI:
```bash
mongo
use reddit_db
db.posts.find().pretty()
```

---

## 🛠 Scripts

- `reddit_producer.py` – Connects to Reddit API and sends messages to Kafka.
- `spark_streaming.py` – Reads from Kafka topic and writes to MongoDB.
- `docker-compose.yml` – Spins up all required services.

---

## 📌 Notes
- All services are containerized for consistency across environments.
- Ensure port conflicts are resolved (especially for Kafka and MongoDB).
- MongoDB data can be persisted using Docker volumes.
