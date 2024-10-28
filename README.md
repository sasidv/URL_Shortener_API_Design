# URL_Shortner_API
This repository contains a URL Shortner API designed to create a unique short URL given a long URL, redirect the users to the original URL when the short URL is accessed and supports automatic expirations of URLs after a set period.

## Functional Requirements
The URL Shortener API supports the following key features:
1. **URL Shortening**: Generates a unique, shortened URL for each given long URL.
2. **Redirection**: When a user accesses a short URL, they are redirected to the original long URL.
3. **Expiration**: The short URLs will expire after a configurable period (e.g., one year).

## Assumptions
We assume that each user will generate a short link only once for a given long URL. Based on this assumption, the server will create a new, unique short URL for every new long link it encounters. However, if this assumption is not upheld, it could result in a denial of service attack, which should be addressed by a separate security layer.

## System Capacity Estimations
Suppose that the system has to handle 100 million short URL creation requests per month. Assuming 100:1 read to write ratio, the system must handle approximately 4000 short URL read requests per second. Assuming that short URLs will have an expiration time of 1 year, the system need to store a unique map of (100*12) million  short URLs per year, which is 1.2 billion URLs in total. Using base64 encoding scheme with a 6-character length allows for approximately 68 billion unique short URL possibilities giving sufficient room for collision handling. 

## System Storage Estimations
Assuming that long URL size is around 2kB, and the remaining storage requirement for short URL,  and expiration date are comparatively negligible, the total system storage requirements for 1 year is (1.2billion * 2kB) around 2.4 TB.

## High-Level Architecture
The system comprises the following key components:

<img width="877" alt="image" src="https://github.com/user-attachments/assets/24eeb799-8a1b-48d7-b05e-da238e131e75">

- Client: A web interface where users can input long URLs and retrieve a short URLs and vise-versa.
  
- Server: Handles business logic including URL shortening, redirection, and expiration.
  
- Database: Stores the mappings between short URLs and long URLs, along with expiration times.

We utilize the Flask API framework to simulate both the server and the client, allowing the client to interact with the server via POST and GET requests. The server processes these requests based on the order they receive and return the output URL links. The choice of database depend on the scalability and availability requirements of the service. The SQL databases are known for keeping track of complex relational data, and maintaining good ACID (Atomocity, Concistency, Isolation and Durability) properties. Whereas no-SQL databases are easy to scale and can support higher read/write request ratio. For this project, starting with an SQL database allows for consistency, simplicity, and ease of development. However, as traffic grows, migrating the URL mappings to a NoSQL database like MongoDB for horizontal scalability could be considered for handling billions of requests efficiently.

## Database Design
The database stores mappings of short URLs to long URLs and other metadata such as expiration time.

| Column         | Type   | Description                                |
|----------------|--------|--------------------------------------------|
| short_url      | string | Unique short URL (6 characters, base64)     |
| long_url       | text   | Original long URL (up to 2 kB)              |
| expiration_time    | datetime   | Expiration timestamp of the short URL            |

## Handelling Hash Collisions
One aspect we considered in implementing the URL shortener API is hash collisions that may occur when two distinct long URLs produce the same short URL (hash), which can lead to incorrect redirections. To effectively prevent this issue, first we used a more robust hashing algorithm 'sha256', which is known for better resistance to collisions compared to other algorithms such as md5. Furthermore we implement a counter-based collision resolution mechanism; before inserting a new short URL into the database, we check for existing entries. If a collision is detected, we append a counter to the original URL to generate a new unique hash, ensuring that each short URL remains distinct.

## SQL Database in-memory Caching
To enhance performance and reduce the frequency of database accesses for redirection requests, we implement an in-memory caching layer using an LRU (least recently used) cache strategy. This in-memory cache will store the mappings of recently accessed short URLs, while removing the oldest accessed once when the space is limited. This helps maintain a relevant subset of data in memory allowing fast access.

## SQL Database Connection Pooling
We implemented SQL database connection pooling to reduce overhead and manage connections efficiently. This allows the system to reuse active connections, improving performance and handling high traffic with lower latency.We implemented database pooling with the aim of reducing database overhead and managing connections effectively under high load conditions.

## **Disaster Recovery**  
The system ensures data integrity through automated backups of the database at regular intervals. Although the cache is lost during an application crash, all URL mappings remain safely stored in the database, ensuring uninterrupted operation. The cache will rebuild incrementally as new requests are processed after the system restarts.

## Future Enhancement suggestions to Support Operational Requirements
To ensure smooth operation at scale, we suggest following improvements:
- **High Availability**: The service must be resilient, ensuring uptime even during traffic spikes or server failures.
  - i) **Load Balancing**: Implement load balancers to distribute incoming traffic across multiple server instances. This approach will improve response times and ensure that no single server becomes a bottleneck during peak usage
  - ii) **Distributed Caching**: To reduce the load on the database and achieve fast redirection times, we can leverage a sophisticated caching layer such as Redis to cache most frequently accessed URLs.
  - iii) **Database Replication**: Set up database replication to ensure that data is redundantly stored across multiple instances. This helps maintain availability even if one database node fails. If the replications can be done accross different regions, users can be directed to access the data closer to their geogrophical location.

- **Scalability**: The system must handle increasing volumes of both URL creation and redirection requests.
  - i) **Database Sharding**: Implement database partitioning to distribute the data across multiple database servers, for example parition data based on the first letter of the short URL hash. This allows the system to handle larger datasets and a higher number of concurrent requests.
  - ii) **Use an easy to scale Database**: The database should be scalable to handle a large number of URLs and clicks. We can upgrade to NoSQL databases such as MongoDB or Cassandra, which are highly scalable and can handle large amounts of data across distributed nodes as well as performs better in high-read traffic applications such as URL redirection.
  - iii) **Asynchronous Programming**: Asynchronous handling ensures the system processes multiple requests concurrently, avoiding delays caused by blocking operations like database queries or API calls. This approach allows the server to remain responsive by continuing to process other requests while waiting for operations to complete, improving scalability and resource efficiency.

## Folder Structure
- The **src** folder contains the following
  - i) **client** folder - Handles client side interactions, specifically for submitting POST and GET requests.
  - ii) **server** folder - Contains the core Server API, manages database operations, and performs URL input validation.
- iii) The **test** Contains unit tests designed to validate API methods and ensure functionality.

## Instructions to run directly from the git clone
  - Clone the repository
```bash
 git clone https://github.com/sasidv/URL_Shortener_API_Design.git
```
  - Install the dependencies
```bash
pip install -r requirements.txt
```
  - Install MySQL, and start a new MySQL connection with the name TEST.
    
  - Start the Flask API Server
```bash
python src/server/server.py.
```
  - Run the Client
```bash
python src/client/client_simple.py.
```
  - Run unit tests
```bash
python src/test/server/test_server.py
python src/test/server/test_validate.py
```
## Instructions to run in docker
Plase check [README_DOCKER.md](https://github.com/sasidv/URL_Shortener_API_Design/blob/main/README_DOCKER.md)
