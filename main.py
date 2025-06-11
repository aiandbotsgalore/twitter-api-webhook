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

# USER ENDPOINTS
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
def get_users_by_ids(params):
    ids = params.get("ids")
    if not ids:
        return jsonify({"error": "Missing required parameter: ids"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/get-users",
            headers=get_headers(),
            params={"ids": ids}
        )
        log_request("get_users_by_ids", params, response.status_code)
        return handle_rapidapi_response(response, "get_users_by_ids")
    except Exception as e:
        logger.error(f"Exception in get_users_by_ids: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_users_by_ids_v2(params):
    rest_ids = params.get("rest_ids")
    if not rest_ids:
        return jsonify({"error": "Missing required parameter: rest_ids"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/get-users-v2",
            headers=get_headers(),
            params={"rest_ids": rest_ids}
        )
        log_request("get_users_by_ids_v2", params, response.status_code)
        return handle_rapidapi_response(response, "get_users_by_ids_v2")
    except Exception as e:
        logger.error(f"Exception in get_users_by_ids_v2: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_replies(params):
    user_id = params.get("user") or params.get("user_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not user_id:
        return jsonify({"error": "Missing required parameter: user or user_id"}), 400
    
    try:
        request_params = {"user": user_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/user-replies",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_user_replies", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_replies")
    except Exception as e:
        logger.error(f"Exception in get_user_replies: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_replies_v2(params):
    user_id = params.get("user") or params.get("user_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not user_id:
        return jsonify({"error": "Missing required parameter: user or user_id"}), 400
    
    try:
        request_params = {"user": user_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/user-replies-v2",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_user_replies_v2", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_replies_v2")
    except Exception as e:
        logger.error(f"Exception in get_user_replies_v2: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_media(params):
    user_id = params.get("user") or params.get("user_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not user_id:
        return jsonify({"error": "Missing required parameter: user or user_id"}), 400
    
    try:
        request_params = {"user": user_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/user-media",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_user_media", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_media")
    except Exception as e:
        logger.error(f"Exception in get_user_media: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_tweets(params):
    user_id = params.get("user") or params.get("user_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not user_id:
        return jsonify({"error": "Missing required parameter: user or user_id"}), 400
    
    try:
        request_params = {"user": user_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/user-tweets",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_user_tweets", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_tweets")
    except Exception as e:
        logger.error(f"Exception in get_user_tweets: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_followings(params):
    user_id = params.get("user") or params.get("user_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not user_id:
        return jsonify({"error": "Missing required parameter: user or user_id"}), 400
    
    try:
        request_params = {"user": user_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/followings",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_user_followings", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_followings")
    except Exception as e:
        logger.error(f"Exception in get_user_followings: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_following_ids(params):
    username = params.get("username")
    count = params.get("count", "5000")
    cursor = params.get("cursor")
    
    if not username:
        return jsonify({"error": "Missing required parameter: username"}), 400
    
    try:
        request_params = {"username": username, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/following-ids",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_user_following_ids", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_following_ids")
    except Exception as e:
        logger.error(f"Exception in get_user_following_ids: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_followers(params):
    user_id = params.get("user") or params.get("user_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not user_id:
        return jsonify({"error": "Missing required parameter: user or user_id"}), 400
    
    try:
        request_params = {"user": user_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/followers",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_user_followers", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_followers")
    except Exception as e:
        logger.error(f"Exception in get_user_followers: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_followers_ids(params):
    username = params.get("username")
    count = params.get("count", "5000")
    cursor = params.get("cursor")
    
    if not username:
        return jsonify({"error": "Missing required parameter: username"}), 400
    
    try:
        request_params = {"username": username, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/followers-ids",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_user_followers_ids", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_followers_ids")
    except Exception as e:
        logger.error(f"Exception in get_user_followers_ids: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_verified_followers(params):
    user_id = params.get("user") or params.get("user_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not user_id:
        return jsonify({"error": "Missing required parameter: user or user_id"}), 400
    
    try:
        request_params = {"user": user_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/verified-followers",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_user_verified_followers", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_verified_followers")
    except Exception as e:
        logger.error(f"Exception in get_user_verified_followers: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_highlights(params):
    user_id = params.get("user") or params.get("user_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not user_id:
        return jsonify({"error": "Missing required parameter: user or user_id"}), 400
    
    try:
        request_params = {"user": user_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/highlights",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_highlights", params, response.status_code)
        return handle_rapidapi_response(response, "get_highlights")
    except Exception as e:
        logger.error(f"Exception in get_highlights: {e}")
        return jsonify({"error": "Internal server error"}), 500

# POSTS ENDPOINTS
@rate_limit_decorator
def get_post_comments(params):
    pid = params.get("pid") or params.get("post_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not pid:
        return jsonify({"error": "Missing required parameter: pid or post_id"}), 400
    
    try:
        request_params = {"pid": pid, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/comments",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_post_comments", params, response.status_code)
        return handle_rapidapi_response(response, "get_post_comments")
    except Exception as e:
        logger.error(f"Exception in get_post_comments: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_post_comments_v2(params):
    pid = params.get("pid") or params.get("post_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not pid:
        return jsonify({"error": "Missing required parameter: pid or post_id"}), 400
    
    try:
        request_params = {"pid": pid, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/comments-v2",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_post_comments_v2", params, response.status_code)
        return handle_rapidapi_response(response, "get_post_comments_v2")
    except Exception as e:
        logger.error(f"Exception in get_post_comments_v2: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_post_quotes(params):
    pid = params.get("pid") or params.get("post_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not pid:
        return jsonify({"error": "Missing required parameter: pid or post_id"}), 400
    
    try:
        request_params = {"pid": pid, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/quotes",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_post_quotes", params, response.status_code)
        return handle_rapidapi_response(response, "get_post_quotes")
    except Exception as e:
        logger.error(f"Exception in get_post_quotes: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_post_retweets(params):
    pid = params.get("pid") or params.get("post_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not pid:
        return jsonify({"error": "Missing required parameter: pid or post_id"}), 400
    
    try:
        request_params = {"pid": pid, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/retweets",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_post_retweets", params, response.status_code)
        return handle_rapidapi_response(response, "get_post_retweets")
    except Exception as e:
        logger.error(f"Exception in get_post_retweets: {e}")
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
def get_tweet_details_v2(params):
    tweet_id = params.get("tweet_id") or params.get("pid")
    
    if not tweet_id:
        return jsonify({"error": "Missing required parameter: tweet_id or pid"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/tweet-v2",
            headers=get_headers(),
            params={"pid": tweet_id}
        )
        log_request("get_tweet_details_v2", params, response.status_code)
        return handle_rapidapi_response(response, "get_tweet_details_v2")
    except Exception as e:
        logger.error(f"Exception in get_tweet_details_v2: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_tweets_by_ids(params):
    ids = params.get("ids")
    
    if not ids:
        return jsonify({"error": "Missing required parameter: ids"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/tweet-by-ids",
            headers=get_headers(),
            params={"ids": ids}
        )
        log_request("get_tweets_by_ids", params, response.status_code)
        return handle_rapidapi_response(response, "get_tweets_by_ids")
    except Exception as e:
        logger.error(f"Exception in get_tweets_by_ids: {e}")
        return jsonify({"error": "Internal server error"}), 500

# SEARCH/EXPLORE ENDPOINTS
@rate_limit_decorator
def search_twitter(params):
    query = params.get("query")
    tweet_type = params.get("type", "Top")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400
    
    try:
        request_params = {
            "query": query,
            "type": tweet_type,
            "count": count
        }
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/search",
            headers=get_headers(),
            params=request_params
        )
        log_request("search_twitter", params, response.status_code)
        return handle_rapidapi_response(response, "search_twitter")
    except Exception as e:
        logger.error(f"Exception in search_twitter: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def search_twitter_v2(params):
    query = params.get("query")
    tweet_type = params.get("type", "Top")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400
    
    try:
        request_params = {
            "query": query,
            "type": tweet_type,
            "count": count
        }
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/search-v2",
            headers=get_headers(),
            params=request_params
        )
        log_request("search_twitter_v2", params, response.status_code)
        return handle_rapidapi_response(response, "search_twitter_v2")
    except Exception as e:
        logger.error(f"Exception in search_twitter_v2: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def autocomplete(params):
    query = params.get("query")
    
    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/autocomplete",
            headers=get_headers(),
            params={"query": query}
        )
        log_request("autocomplete", params, response.status_code)
        return handle_rapidapi_response(response, "autocomplete")
    except Exception as e:
        logger.error(f"Exception in autocomplete: {e}")
        return jsonify({"error": "Internal server error"}), 500

# SPACES ENDPOINT
@rate_limit_decorator
def get_space_details(params):
    space_id = params.get("id") or params.get("space_id")
    
    if not space_id:
        return jsonify({"error": "Missing required parameter: id or space_id"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/spaces",
            headers=get_headers(),
            params={"id": space_id}
        )
        log_request("get_space_details", params, response.status_code)
        return handle_rapidapi_response(response, "get_space_details")
    except Exception as e:
        logger.error(f"Exception in get_space_details: {e}")
        return jsonify({"error": "Internal server error"}), 500

# ORGANIZATION ENDPOINT
@rate_limit_decorator
def get_organization_affiliates(params):
    org_id = params.get("id") or params.get("org_id")
    
    if not org_id:
        return jsonify({"error": "Missing required parameter: id or org_id"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/org-affiliates",
            headers=get_headers(),
            params={"id": org_id}
        )
        log_request("get_organization_affiliates", params, response.status_code)
        return handle_rapidapi_response(response, "get_organization_affiliates")
    except Exception as e:
        logger.error(f"Exception in get_organization_affiliates: {e}")
        return jsonify({"error": "Internal server error"}), 500

# LISTS ENDPOINTS
@rate_limit_decorator
def search_lists(params):
    query = params.get("query")
    
    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/search-lists",
            headers=get_headers(),
            params={"query": query}
        )
        log_request("search_lists", params, response.status_code)
        return handle_rapidapi_response(response, "search_lists")
    except Exception as e:
        logger.error(f"Exception in search_lists: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_list_details(params):
    list_id = params.get("listId") or params.get("list_id")
    
    if not list_id:
        return jsonify({"error": "Missing required parameter: listId or list_id"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/list-details",
            headers=get_headers(),
            params={"listId": list_id}
        )
        log_request("get_list_details", params, response.status_code)
        return handle_rapidapi_response(response, "get_list_details")
    except Exception as e:
        logger.error(f"Exception in get_list_details: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_list_timeline(params):
    list_id = params.get("listId") or params.get("list_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not list_id:
        return jsonify({"error": "Missing required parameter: listId or list_id"}), 400
    
    try:
        request_params = {"listId": list_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/list-timeline",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_list_timeline", params, response.status_code)
        return handle_rapidapi_response(response, "get_list_timeline")
    except Exception as e:
        logger.error(f"Exception in get_list_timeline: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_list_followers(params):
    list_id = params.get("listId") or params.get("list_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not list_id:
        return jsonify({"error": "Missing required parameter: listId or list_id"}), 400
    
    try:
        request_params = {"listId": list_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/list-followers",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_list_followers", params, response.status_code)
        return handle_rapidapi_response(response, "get_list_followers")
    except Exception as e:
        logger.error(f"Exception in get_list_followers: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_list_members(params):
    list_id = params.get("listId") or params.get("list_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not list_id:
        return jsonify({"error": "Missing required parameter: listId or list_id"}), 400
    
    try:
        request_params = {"listId": list_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/list-members",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_list_members", params, response.status_code)
        return handle_rapidapi_response(response, "get_list_members")
    except Exception as e:
        logger.error(f"Exception in get_list_members: {e}")
        return jsonify({"error": "Internal server error"}), 500

# COMMUNITY ENDPOINTS
@rate_limit_decorator
def search_community(params):
    query = params.get("query")
    
    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/search-community",
            headers=get_headers(),
            params={"query": query}
        )
        log_request("search_community", params, response.status_code)
        return handle_rapidapi_response(response, "search_community")
    except Exception as e:
        logger.error(f"Exception in search_community: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_community_topics(params):
    try:
        response = requests.get(
            f"{BASE_URL}/community-topics",
            headers=get_headers()
        )
        log_request("get_community_topics", params, response.status_code)
        return handle_rapidapi_response(response, "get_community_topics")
    except Exception as e:
        logger.error(f"Exception in get_community_topics: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def fetch_popular_community(params):
    try:
        response = requests.get(
            f"{BASE_URL}/fetch-popular-community",
            headers=get_headers()
        )
        log_request("fetch_popular_community", params, response.status_code)
        return handle_rapidapi_response(response, "fetch_popular_community")
    except Exception as e:
        logger.error(f"Exception in fetch_popular_community: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_community_timeline(params):
    try:
        response = requests.get(
            f"{BASE_URL}/explore-community-timeline",
            headers=get_headers()
        )
        log_request("get_community_timeline", params, response.status_code)
        return handle_rapidapi_response(response, "get_community_timeline")
    except Exception as e:
        logger.error(f"Exception in get_community_timeline: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_community_members(params):
    community_id = params.get("communityId") or params.get("community_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not community_id:
        return jsonify({"error": "Missing required parameter: communityId or community_id"}), 400
    
    try:
        request_params = {"communityId": community_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/community-members",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_community_members", params, response.status_code)
        return handle_rapidapi_response(response, "get_community_members")
    except Exception as e:
        logger.error(f"Exception in get_community_members: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_community_moderators(params):
    community_id = params.get("communityId") or params.get("community_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not community_id:
        return jsonify({"error": "Missing required parameter: communityId or community_id"}), 400
    
    try:
        request_params = {"communityId": community_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/community-moderators",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_community_moderators", params, response.status_code)
        return handle_rapidapi_response(response, "get_community_moderators")
    except Exception as e:
        logger.error(f"Exception in get_community_moderators: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_community_tweets(params):
    community_id = params.get("communityId") or params.get("community_id")
    tweet_type = params.get("type", "Top")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not community_id:
        return jsonify({"error": "Missing required parameter: communityId or community_id"}), 400
    
    try:
        request_params = {
            "communityId": community_id,
            "type": tweet_type,
            "count": count
        }
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/community-tweets",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_community_tweets", params, response.status_code)
        return handle_rapidapi_response(response, "get_community_tweets")
    except Exception as e:
        logger.error(f"Exception in get_community_tweets: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_community_about(params):
    community_id = params.get("communityId") or params.get("community_id")
    
    if not community_id:
        return jsonify({"error": "Missing required parameter: communityId or community_id"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/community-about",
            headers=get_headers(),
            params={"communityId": community_id}
        )
        log_request("get_community_about", params, response.status_code)
        return handle_rapidapi_response(response, "get_community_about")
    except Exception as e:
        logger.error(f"Exception in get_community_about: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_community_details(params):
    community_id = params.get("communityId") or params.get("community_id")
    
    if not community_id:
        return jsonify({"error": "Missing required parameter: communityId or community_id"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/community-details",
            headers=get_headers(),
            params={"communityId": community_id}
        )
        log_request("get_community_details", params, response.status_code)
        return handle_rapidapi_response(response, "get_community_details")
    except Exception as e:
        logger.error(f"Exception in get_community_details: {e}")
        return jsonify({"error": "Internal server error"}), 500

# JOBS ENDPOINTS
@rate_limit_decorator
def search_job_locations(params):
    query = params.get("query")
    
    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/jobs-locations-suggest",
            headers=get_headers(),
            params={"query": query}
        )
        log_request("search_job_locations", params, response.status_code)
        return handle_rapidapi_response(response, "search_job_locations")
    except Exception as e:
        logger.error(f"Exception in search_job_locations: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def search_jobs(params):
    query = params.get("query")
    location = params.get("location")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400
    
    try:
        request_params = {"query": query, "count": count}
        if location:
            request_params["location"] = location
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/jobs-search",
            headers=get_headers(),
            params=request_params
        )
        log_request("search_jobs", params, response.status_code)
        return handle_rapidapi_response(response, "search_jobs")
    except Exception as e:
        logger.error(f"Exception in search_jobs: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_job_details(params):
    job_id = params.get("jobId") or params.get("job_id")
    
    if not job_id:
        return jsonify({"error": "Missing required parameter: jobId or job_id"}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/job-details",
            headers=get_headers(),
            params={"jobId": job_id}
        )
        log_request("get_job_details", params, response.status_code)
        return handle_rapidapi_response(response, "get_job_details")
    except Exception as e:
        logger.error(f"Exception in get_job_details: {e}")
        return jsonify({"error": "Internal server error"}), 500

# TRENDS ENDPOINTS
@rate_limit_decorator
def get_trends_locations(params):
    try:
        response = requests.get(
            f"{BASE_URL}/trends-locations",
            headers=get_headers()
        )
        log_request("get_trends_locations", params, response.status_code)
        return handle_rapidapi_response(response, "get_trends_locations")
    except Exception as e:
        logger.error(f"Exception in get_trends_locations: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_trends_by_location(params):
    woeid = params.get("woeid", "1")  # Default to worldwide
    
    try:
        response = requests.get(
            f"{BASE_URL}/trends-by-location",
            headers=get_headers(),
            params={"woeid": woeid}
        )
        log_request("get_trends_by_location", params, response.status_code)
        return handle_rapidapi_response(response, "get_trends_by_location")
    except Exception as e:
        logger.error(f"Exception in get_trends_by_location: {e}")
        return jsonify({"error": "Internal server error"}), 500

# DEPRECATED ENDPOINTS
@rate_limit_decorator
def get_post_likes(params):
    pid = params.get("pid") or params.get("post_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not pid:
        return jsonify({"error": "Missing required parameter: pid or post_id"}), 400
    
    try:
        request_params = {"pid": pid, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/likes",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_post_likes", params, response.status_code)
        return handle_rapidapi_response(response, "get_post_likes")
    except Exception as e:
        logger.error(f"Exception in get_post_likes: {e}")
        return jsonify({"error": "Internal server error"}), 500

@rate_limit_decorator
def get_user_likes(params):
    user_id = params.get("user") or params.get("user_id")
    count = params.get("count", "20")
    cursor = params.get("cursor")
    
    if not user_id:
        return jsonify({"error": "Missing required parameter: user or user_id"}), 400
    
    try:
        request_params = {"user": user_id, "count": count}
        if cursor:
            request_params["cursor"] = cursor
            
        response = requests.get(
            f"{BASE_URL}/user-likes",
            headers=get_headers(),
            params=request_params
        )
        log_request("get_user_likes", params, response.status_code)
        return handle_rapidapi_response(response, "get_user_likes")
    except Exception as e:
        logger.error(f"Exception in get_user_likes: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Complete action map with all 48 endpoints
ACTION_MAP = {
    # User Endpoints (13)
    "get_user_by_username": get_user_by_username,
    "get_users_by_ids": get_users_by_ids,
    "get_users_by_ids_v2": get_users_by_ids_v2,
    "get_user_replies": get_user_replies,
    "get_user_replies_v2": get_user_replies_v2,
    "get_user_media": get_user_media,
    "get_user_tweets": get_user_tweets,
    "get_user_followings": get_user_followings,
    "get_user_following_ids": get_user_following_ids,
    "get_user_followers": get_user_followers,
    "get_user_followers_ids": get_user_followers_ids,
    "get_user_verified_followers": get_user_verified_followers,
    "get_highlights": get_highlights,
    
    # Posts Endpoints (7)
    "get_post_comments": get_post_comments,
    "get_post_comments_v2": get_post_comments_v2,
    "get_post_quotes": get_post_quotes,
    "get_post_retweets": get_post_retweets,
    "get_tweet_details": get_tweet_details,
    "get_tweet_details_v2": get_tweet_details_v2,
    "get_tweets_by_ids": get_tweets_by_ids,
    
    # Search/Explore Endpoints (3)
    "search_twitter": search_twitter,
    "search_twitter_v2": search_twitter_v2,
    "autocomplete": autocomplete,
    
    # Spaces Endpoint (1)
    "get_space_details": get_space_details,
    
    # Organization Endpoint (1)
    "get_organization_affiliates": get_organization_affiliates,
    
    # Lists Endpoints (5)
    "search_lists": search_lists,
    "get_list_details": get_list_details,
    "get_list_timeline": get_list_timeline,
    "get_list_followers": get_list_followers,
    "get_list_members": get_list_members,
    
    # Community Endpoints (9)
    "search_community": search_community,
    "get_community_topics": get_community_topics,
    "fetch_popular_community": fetch_popular_community,
    "get_community_timeline": get_community_timeline,
    "get_community_members": get_community_members,
    "get_community_moderators": get_community_moderators,
    "get_community_tweets": get_community_tweets,
    "get_community_about": get_community_about,
    "get_community_details": get_community_details,
    
    # Jobs Endpoints (3)
    "search_job_locations": search_job_locations,
    "search_jobs": search_jobs,
    "get_job_details": get_job_details,
    
    # Trends Endpoints (2)
    "get_trends_locations": get_trends_locations,
    "get_trends_by_location": get_trends_by_location,
    
    # Deprecated Endpoints (2)
    "get_post_likes": get_post_likes,
    "get_user_likes": get_user_likes
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
        "available_actions": list(ACTION_MAP.keys()),
        "total_endpoints": len(ACTION_MAP)
    })

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "service": "Twitter241 API Webhook",
        "endpoints": ["/twitter", "/health"],
        "total_available_actions": len(ACTION_MAP),
        "available_actions": list(ACTION_MAP.keys()),
        "usage": "POST to /twitter with JSON body containing 'action' and 'params' fields"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
