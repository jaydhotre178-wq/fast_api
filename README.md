initializing project :  uv init  . 

What is an endpoint?
An endpoint is a specific URL (plus HTTP method) in your API that does one thing when someone requests it.

Think of your API as a building with many doors. Each door:

Has an address (the URL path, like /items/5)

Has a sign on it saying what it's for (the HTTP method: GET, POST, etc.)

Leads to one specific room (the function that runs)


In FastAPI, you create an endpoint with a decorator:

python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
Let's dissect this:

Piece	Meaning
@app.get(...)	The HTTP method — GET means "read/fetch data"
"/items/{item_id}"	The path — the URL pattern
def get_item(...)	The handler function — code that runs when this endpoint is hit
{item_id}	A path parameter — a variable part of the URL
So the endpoint is the whole thing: method + path + the function that handles it.

Endpoints in action
If your app has these:

python
@app.get("/users")          # List all users
@app.get("/users/{id}")     # Get one user
@app.post("/users")         # Create a new user
@app.delete("/users/{id}")  # Delete a user
That's 4 endpoints. Notice /users appears three times — but with different methods, they're different endpoints. The method is part of the identity.


What is Uvicorn?
Uvicorn is a web server. Specifically, it's a fast, production-ready ASGI server for Python.

What does "ASGI" mean?
WSGI (Web Server Gateway Interface) = the old standard for Python web apps (used by Flask, Django historically). It's synchronous — handles one request at a time per worker.

ASGI (Asynchronous Server Gateway Interface) = the modern standard. It's asynchronous — can handle many requests concurrently, supports WebSockets, and works with async/await.

