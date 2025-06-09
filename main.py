from flask import Flask, request, jsonify
import requests
import os
import logging
import time
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
RAPIDAPI_HOST = "twitter241.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}"

# Rate limiting tracker
last_request_time = 0
MIN_REQUEST_INTERVAL = 1.2  # Minimum seconds between requests for BASIC plan

def rate_limit_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global last_request_time
        current_time = time.time()
        
        # Enforce minimum interval between requests
        time_since_last = current_time - last_request_time
        if time_since_last < MIN_REQUEST_INTERVAL:
            sleep_time = MIN_REQUEST_INTERVAL - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        last_request_time = time.time()
        return func(*args, **kwargs)
    return wrapper

# Headers for all RapidAPI requests
def get_headers():
    return {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

def log_request(action, params, response_status):
    timestamp = datetime.now().isoformat()
    logger.info(f"[{timestamp}] Action: {action}, Params: {params}, Status: {response_status}")

def handle_rapidapi_response(response, action):
    if response.status_code == 200:
        return jsonify(response.json()), 200
    elif response.status_code == 429:
        logger.warning(f"Rate limit hit for {action} - user should try again later")
        return jsonify({
            "error": "Rate limit exceeded. Twitter API calls are limited on the BASIC plan.", 
            "suggestion": "Please wait a moment and try again, or consider upgrading your RapidAPI plan.",
            "status": "rate_limited"
        }), 429
    elif response.status_code == 401:
        return jsonify({"error": "Invalid API key or authentication failed."}), 401
    else:
        logger.error(f"RapidAPI error for {action}: {response.status_code} - {response.text}")
        return jsonify({"error": f"API request failed with status {response.status_code}"}), response.status_code

@rate_limit_decorator
def search_twitter(params):
    query = params.get("query")
    tweet_type = params.get("type", "Top")
    count = params.get("count", "10")
    
    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/search",
            headers=get_headers(),
            params={
                "query": query,
                "type": tweet_type,
                "count": count
            }
        )
        log_request("search_twitter", params, response.status_code)
        return handle_rapidapi_response(response, "search_twitter")
    except Exception as e:
        logger.error(f"Exception in search_twitter: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_by_username(params):
    username = params.get("username")
    
    if not username:
        return jsonify({"error": "Missing required parameter: username"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/user",
            headers=get_headers(),
            params={"username": username}
        )
        log_request("get_user_by_username", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_by_username")
    except Exception as e:
        logger.error(f"Exception in get_user_by_username: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_tweet_details(params):
    tweet_id = params.get("tweet_id") or params.get("pid")
    
    if not tweet_id:
        return jsonify({"error": "Missing required parameter: tweet_id or pid"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/tweet",
            headers=get_headers(),
            params={"pid": tweet_id}
        )
        log_request("get_tweet_details", params, response.status_code)
        return handle_rapidapi_response(response, "get_tweet_details")
    except Exception as e:
        logger.error(f"Exception in get_tweet_details: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_tweets(params):
    user_id = params.get("user_id") or params.get("user")
    count = params.get("count", "10")
    
    if not user_id:
        return jsonify({"error": "Missing required parameter: user_id or user"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/user-tweets",
            headers=get_headers(),
            params={
                "user": user_id,
                "count": count
            }
        )
        log_request("get_user_tweets", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_tweets")
    except Exception as e:
        logger.error(f"Exception in get_user_tweets: {e}")
        return jsonify({"error": "Internal server error"}), 500

ACTION_MAP = {
    "search_twitter": search_twitter,
    "get_user_by_username": get_user_by_username,
    "get_tweet_details": get_tweet_details,
    "get_user_tweets": get_user_tweets
}

@app.route("/twitter", methods=["POST"])
def twitter_router():
    if not RAPIDAPI_KEY:
        return jsonify({"error": "RAPIDAPI_KEY environment variable not set"}), 500
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON in request body"}), 400
    
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400
    
    action = data.get("action")
    params = data.get("params", {})
    
    if not action:
        return jsonify({"error": "Missing required field: action"}), 400
    
    if action not in ACTION_MAP:
        available_actions = list(ACTION_MAP.keys())
        return jsonify({
            "error": f"Invalid action: {action}",
            "available_actions": available_actions
        }), 400
    
    logger.info(f"Executing action: {action} with params: {params}")
    return ACTION_MAP[action](params)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "available_actions": list(ACTION_MAP.keys())
    })

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "service": "Twitter API Webhook",
        "endpoints": ["/twitter", "/health"],
        "available_actions": list(ACTION_MAP.keys()),
        "usage": "POST to /twitter with JSON body containing 'action' and 'params' fields"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)