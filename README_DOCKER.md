## **Instructions to Run the Application in a Docker Container**

1. **Install Docker:**
   - Download and install Docker from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).
   - Follow the installation steps and make sure Docker is running.

2. **Open the Terminal (or Command Prompt on Windows):**

3. **Log in to Docker Hub:**

   Run the following command to log in and enter your Docker Hub credentials:
   ```bash
   docker login
   ```
   If you don't have an account, create one at [https://hub.docker.com](https://hub.docker.com)
 
4. **Pull the Application Image:**

   ```bash
   docker pull shashidoo1990/url_shortener_api:latest
   ```

5. **Run the Application:**

   Use the following command to run the application:

   ```bash
   docker-compose up -d 
   ```

6. **Verify the Application is Running:**

   - **Check if the Containers are Running:**

     ```bash
     docker ps
     ```

     You should see the `url_shortener` container listed. If it’s not listed, the container might have stopped due to an issue.

   - **Check the Logs for Errors:**

     ```bash
     docker logs url_shortener
     ```

     Look for any errors to troubleshoot if the application isn’t working as expected.


7. **Send Requests to Server Using the Client Script:**

Run the following command to execute the `client_simple.py` script inside the container, and test the application by sending requests:

```bash
docker exec -it url_shortener python client_simple.py
```
Expected output 
    
      1. **First POST Request:**
         ```
         # Shortened URL requested for https://example.com: http://localhost:5000/b84236
         ```
         Creates a short URL for `https://example.com`.
      
      2. **First GET Request:**
         ```
        # Original URL after redirect: https://example.com
         Status Code: 200
         ```
         Redirects to the original URL, confirming success with status 200.
      
      3. **Second POST Request:**
         ```
         # Shortened URL requested for https://en.wikipedia.org/wiki/Flask_(web_framework): http://localhost:5000/ca60e0
         ```
         Creates a short URL for the Wikipedia page.

      4. **Third POST Request:**
         ```
         # Shortened URL requested for https://www.techtarget.com/searchdatamanagement/definition/database: http://localhost:5000/cef976
         ```
         Generates a short URL for the TeckTarget page.
         
      5. **Second GET Request:**
         ```
         # Original URL after redirect: https://www.techtarget.com/searchdatamanagement/definition/database
         Status Code: 200
         ```
         Confirms redirection with status 200.
      
      6. **Fourth POST Request:**
         ```
         Expects an error since the domain is prohibited.
         # Shortened URL request: error!
         ```
         Requested a short URL for 'https://facebook.com'. Receives an error since the domain is prohibited.
      
      7. **Another GET Request to Example.com Short URL:**
         ```
         # Original URL after redirect: https://example.com
         Status Code: 200
         ```
         Confirms redirection with status 200.
      
      8. **Fifth POST Request (Example.com again):**
         ```
         # Shortened URL requested for https://example.com: http://localhost:5000/bff0e0
         ```
         Note that this short link is different from the one in step 1 as we create a unique link for each new URL request.
      
      9. **Sixth POST Request (Extremely Long URL):**
         ```
         # Shortened URL request: error!
         ```
         Fails due to exceeding maximum allowed URL length.
      
      10. **Final GET Request to Example.com Short URL:**
         ```
         # Original URL after redirect: https://example.com
         Status Code: 200
         ```
         Confirms redirection with status 200.

 

8. **Stop and Clean Up Containers**

If you’re done with the application, use the following command to stop and remove all containers:

```bash
docker-compose down
```
