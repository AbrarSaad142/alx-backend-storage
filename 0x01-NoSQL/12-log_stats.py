from pymongo import MongoClient

def log_stats():
    # Connect to MongoDB
    client = MongoClient()
    db = client.logs
    nginx_collection = db.nginx

    # Get the total number of logs
    log_count = nginx_collection.count_documents({})

    # Define the methods we are interested in
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    # Print the total number of logs
    print(f"{log_count} logs")

    # Print the count of each method
    print("Methods:")
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count the number of documents where method is GET and path is /status
    status_check_count = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    log_stats()
