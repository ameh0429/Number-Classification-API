import json

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n <= 0:
        return False  # Fix: 0 should not be a perfect number
    return n == sum(i for i in range(1, n) if n % i == 0)

def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]  # Use absolute value to avoid issues
    power = len(digits)
    return n == sum(d**power for d in digits)

def get_fun_fact(n):
    if is_armstrong(n):
        return f"{n} is an Armstrong number because {' + '.join([f'{d}^{len(str(abs(n)))}' for d in str(abs(n))])} = {n}"
    elif is_prime(n):
        return f"{n} is a prime number because it has only two divisors: 1 and itself."
    elif is_perfect(n):
        return f"{n} is a perfect number because the sum of its proper divisors equals the number."
    else:
        return f"{n} is just an interesting number!"

def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters", {})
        num_str = query_params.get("number", "")

        # Validate input: number must be a valid integer or float
        try:
            num = float(num_str) if "." in num_str else int(num_str)
        except ValueError:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"number": num_str, "error": True})
            }

        # Construct response data
        response = {
            "number": num,
            "is_prime": is_prime(int(num)),  # Convert to int for prime check
            "is_perfect": is_perfect(int(num)),  # Convert to int for perfect check
            "properties": ["odd" if int(num) % 2 else "even"],
            "digit_sum": sum(int(d) for d in str(abs(int(num)))),
            "fun_fact": get_fun_fact(int(num))
        }

        if is_armstrong(int(num)):
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
