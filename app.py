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
