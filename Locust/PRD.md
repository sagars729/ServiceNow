# Performance Testing With Locust

This performance test uses Locust to test the performance of ESSR: https://app.essr.qa.umd.edu/rw

## Prerequisites
1. Install [Python3](https://www.python.org/downloads/). 
2. Install Locust
```bash
pip install locustio
```
3. Create a file for the authorization key
```bash
touch auth.txt
echo "your_key_here" > auth.txt
```

## Modify The Update Form JSON
1. Update the form manually using the PRD interface. 
2. Inspect the network requests and copy the outgoing post request's body as the body in the program. 
3. Update the body with the correct data.
```python
body = {}
```
**IT IS CRUCIAL THAT YOU UPDATE THE DATE IN THE BODY TO REFLECT THE DATE RECEIVED FROM YOUR MANUAL REQUEST EVERY TIME YOU RUN THIS TEST**. Failure to do so will result in an Internal Server Error. The test will handle all subsequent date changes on its own but it will not handle the initial one. 
4. Update any of the default employee, supervisor, and next supervisor - currently set to me, Vladamir Labar, and William Gomes

## Running The Test
1. Run locust in the command line
```bash
locust
```
2. Navigate to localhost:8089/
3. Enter the number of locusts to generate and their hatch rate
4. Enter https://itprd.dev.umd.edu as the host and click "Start Swarming"
