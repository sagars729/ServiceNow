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

## Running The Test
1. Run locust in the command line
```bash
locust
```
2. Navigate to localhost:8089/
3. Enter the number of locusts to generate and their hatch rate
4. Enter https://app.essr.qa.umd.edu as the host and click "Start Swarming"
