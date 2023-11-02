from flask import Flask, Response
import os
import multiprocessing
import random
import string

app = Flask(__name__)

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

@app.route('/stress_test/<int:threads>/<int:calculations>', methods=['GET'])
def cpu_test(threads, calculations):
    results = []
    processes = []

    def stress_func(calcs):
        thread_results = [fibonacci(500) for _ in range(calcs)]
        return thread_results

    for _ in range(threads):
        process = multiprocessing.Process(target=stress_func, args=(calculations,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return f"Stress test complete: {threads} threads each performing {calculations} calculations."

@app.route('/')
def index():
    return """
    <h1>Navigation Links</h1>
    <ul>
        <li><a href="/stress_test/4/10">Stress Test 1 (4/10)</a></li>
        <li><a href="/stress_test/1024">Stress Test 2 (1024)</a></li>
        <li><a href="/generate_data/1024">Generate Data (1024)</a></li>
    </ul>
    """

@app.route('/stress_test/<int:size>')
def stress_test(size):
    file_path = 'stress_test_data.txt'
    size_to_generate = size * 1024 * 1024  # 1GB

    with open(file_path, 'wb') as file:
        while os.path.getsize(file_path) < size_to_generate:
            file.write(os.urandom(1024))  # Write 1KB of random data at a time

    return Response("Stress test data generation complete.", content_type='text/plain')


# A list to store generated data
data_store = []

# Helper function to generate random data
def generate_random_data(size):
    return ''.join(random.choice(string.ascii_letters) for _ in range(size))

@app.route('/generate_data/<int:size>')
def generate_and_store_data(size):
    # Generate and store random data
    data = generate_random_data(size * 1024 * 1024)  # Generate 'size' MB of data
    data_store.append(data)
    return f"Generated and stored {size} MB of data."

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
