# Building a Number Classification API. MY Stage 1 Task.
## Overview

The Number Classification API is a simple HTTP API that classifies numbers based on their mathematical properties. The API is publicly accessible and deployed using AWS Lambda and API Gateway making it serverless, cost-efficient, and scalable.

## Features
- Determines if a number is prime, even, or odd.
- Supports multiple number classifications in a single request.
- JSON-based responses.
- CORS enabled for public access.

## Architecture Diagram
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b2liu5x419b8f3v6l8fd.png)

## Deployment
This API is deployed using:
- AWS Lambda for serverless execution.
- API Gateway for exposing the endpoint.
- GitHub for version control.

## Technologies Used
- Python (Lambda function)
- AWS Lambda (Serverless execution)
- API Gateway (Public API exposure)
- GitHub (Version control and CI/CD)

## Project Structure

```
Number-Classification-API/
│-- lambda_function.py  # Main Lambda function
│-- requirements.txt    # Python dependencies
│-- README.md           # Project documentation
│-- .gitignore          # Git ignore file
└── app.py              # Python scripts
```

## Set up Instructions 
### Clone the Repository

```
git clone https://github.com/ameh0429/Number-Classification-API.git
cd Number-Classification-API
```

### Create and Activate Virtual Environment
It is best to use a virtual environment to manage dependencies:

```
python -m venv venv
Source venv\Scripts\activate

```

### Install Dependencies

```
pip install flask flask-cors
```

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/p492agd7cajnhkjiiovp.png)

### Create the Flask App
Create a file called app.py in your project folder 

```
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is a perfect number
def is_perfect(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return n == sum(d**power for d in digits)

# Function to generate fun facts
def get_fun_fact(n):
    if is_armstrong(n):
        return f"{n} is an Armstrong number because {' + '.join([f'{d}^{len(str(n))}' for d in str(n)])} = {n}"
    elif is_prime(n):
        return f"{n} is a prime number because it has only two divisors: 1 and itself."
    elif is_perfect(n):
        return f"{n} is a perfect number because the sum of its proper divisors equals the number."
    else:
        return f"{n} is just an interesting number!"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    num = request.args.get('number')

    if not num or not num.isdigit():
        return jsonify({"number": num, "error": True}), 400

    num = int(num)
    
    response = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": ["odd" if num % 2 else "even"],
        "digit_sum": sum(int(d) for d in str(num)),
        "fun_fact": get_fun_fact(num)
    }

    if is_armstrong(num):
        response["properties"].append("armstrong")

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

```

### Run the API Locally

```
python app.py
```

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6spvyicmr50g58idvt0n.png)

Open your browser to test the API:

```
http://127.0.0.1:5000/api/classify-number?number=153
```

JSON Response

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2bn23qo54zs24mj7g8cy.png)

### Deploy the API
Create `lambda_function.py`

```
import json

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return n == sum(d**power for d in digits)

def get_fun_fact(n):
    if is_armstrong(n):
        return f"{n} is an Armstrong number because {' + '.join([f'{d}^{len(str(n))}' for d in str(n)])} = {n}"
    elif is_prime(n):
        return f"{n} is a prime number because it has only two divisors: 1 and itself."
    elif is_perfect(n):
        return f"{n} is a perfect number because the sum of its proper divisors equals the number."
    else:
        return f"{n} is just an interesting number!"

def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters", {})
        num = query_params.get("number", "")

        if not num.isdigit():
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"number": num, "error": True})
            }

        num = int(num)

        response = {
            "number": num,
            "is_prime": is_prime(num),
            "is_perfect": is_perfect(num),
            "properties": ["odd" if num % 2 else "even"],
            "digit_sum": sum(int(d) for d in str(num)),
            "fun_fact": get_fun_fact(num)
        }

        if is_armstrong(num):
            response["properties"].append("armstrong")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }

```

### Package and Deploy to AWS Lambda
- Zip the function and Upload to AWS Lambda

```
zip function.zip lambda_function.py
```

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3f7ot5i5t2sew2f16o1i.png)


### Create an API Gateway
- Choose HTTP API.
- Add Integration → Choose Lambda Function.
- Select your Lambda function (NumberClassifierAPI).
- Enter /api/classify-number as the route.
- Choose GET as the method.
- Then Deploy.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/f5fcz5vrvuki8g3e5bgk.png)

### Test Your API
Once deployed, copy the API Gateway URL and test it in your browser

```
https://3zjuhtikq8.execute-api.us-east-1.amazonaws.com/api/classify-number?number=153
```
Expected JSON Output

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3i4q51qexvp8inubphq9.png)


### Enable CORS in API Gateway

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xcqxf5etoymdok41bwpa.png)

## What I Learned
During the development of this project, I gained experience in:
- Setting up and deploying a serverless API using AWS Lambda and API Gateway.
- Writing Python functions to classify numbers based on mathematical properties.
- Managing CORS configurations for public API access.
- Using GitHub for version control and collaboration.
- Handling API requests and responses in JSON format.
- Troubleshooting deployment issues and refining the API structure.

## Future Improvements
- Add support for multiple numbers in a single request.
- Implement more mathematical classifications (e.g., perfect numbers).
- Improve error handling and validation.
