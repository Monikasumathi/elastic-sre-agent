#!/usr/bin/env python3
"""
Sample Data Generator for Elastic SRE Agent
Generates realistic application logs and GitHub commits for testing.
"""

import json
import random
from datetime import datetime, timedelta

def generate_logs(num_logs=170, num_errors=120):
    """Generate application logs with realistic error patterns."""
    
    services = ["checkout-service", "order-service", "inventory-service", "user-service"]
    levels = ["INFO", "WARN", "ERROR"]
    
    error_messages = [
        "NullPointerException in PaymentProcessor.processOrder()",
        "Connection timeout to payment gateway",
        "Order validation failed - missing required field",
        "Circuit breaker OPEN for payment-service",
        "Payment rollback triggered due to upstream failure",
        "Database connection pool exhausted",
    ]
    
    info_messages = [
        "Request processed successfully",
        "User authentication completed",
        "Cache refreshed",
        "Health check passed",
    ]
    
    logs = []
    base_time = datetime.utcnow()
    
    # Generate error logs (concentrated in checkout-service)
    for i in range(num_errors):
        timestamp = base_time - timedelta(minutes=random.randint(1, 1440))
        
        # 70% of errors in checkout-service (to simulate the outage)
        if random.random() < 0.7:
            service = "checkout-service"
            message = error_messages[0]  # NullPointerException
        else:
            service = random.choice(services)
            message = random.choice(error_messages)
        
        logs.append({
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "level": "ERROR",
            "service": service,
            "message": message,
            "host": f"prod-{service[:4]}-{random.randint(1,5):02d}",
            "trace_id": f"trace-{random.randint(10000, 99999)}"
        })
    
    # Generate normal logs
    for i in range(num_logs - num_errors):
        timestamp = base_time - timedelta(minutes=random.randint(1, 1440))
        logs.append({
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "level": random.choice(["INFO", "WARN"]),
            "service": random.choice(services),
            "message": random.choice(info_messages),
            "host": f"prod-app-{random.randint(1,10):02d}",
            "trace_id": f"trace-{random.randint(10000, 99999)}"
        })
    
    return logs

def generate_commits(bad_commit_id="f9ed964"):
    """Generate GitHub commits including the 'bad' one."""
    
    base_time = datetime.utcnow()
    
    commits = [
        {
            "commit_id": "f8e7d6c",
            "author": "alice",
            "message": "Updated README with new API documentation",
            "files_changed": ["README.md"],
            "service": "documentation",
            "additions": 25,
            "deletions": 10,
            "timestamp": (base_time - timedelta(hours=20)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "branch": "main"
        },
        {
            "commit_id": "b5a4c3d",
            "author": "bob",
            "message": "Fixed typo in user registration email template",
            "files_changed": ["src/templates/email/registration.html"],
            "service": "user-service",
            "additions": 1,
            "deletions": 1,
            "timestamp": (base_time - timedelta(hours=18)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "branch": "main"
        },
        {
            "commit_id": bad_commit_id,  # THE BAD COMMIT
            "author": "devdave",
            "message": "Refactored PaymentProcessor to remove legacy null safety checks for cleaner code",
            "files_changed": ["src/main/java/com/techcorp/checkout/PaymentProcessor.java"],
            "service": "checkout-service",
            "additions": 45,
            "deletions": 72,
            "timestamp": (base_time - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "branch": "main"
        },
        {
            "commit_id": "c9d8e7f",
            "author": "carol",
            "message": "Added new inventory sync endpoint for warehouse integration",
            "files_changed": ["src/main/java/com/techcorp/inventory/SyncController.java"],
            "service": "inventory-service",
            "additions": 89,
            "deletions": 12,
            "timestamp": (base_time - timedelta(hours=15)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "branch": "main"
        },
        {
            "commit_id": "d2e3f4a",
            "author": "devdave",
            "message": "Performance optimization for order history queries",
            "files_changed": ["src/main/java/com/techcorp/order/OrderRepository.java"],
            "service": "order-service",
            "additions": 34,
            "deletions": 28,
            "timestamp": (base_time - timedelta(hours=12)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "branch": "main"
        },
        {
            "commit_id": "e5f6a7b",
            "author": "alice",
            "message": "Updated logging configuration for better observability",
            "files_changed": ["src/main/resources/logback.xml"],
            "service": "infrastructure",
            "additions": 15,
            "deletions": 8,
            "timestamp": (base_time - timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "branch": "main"
        }
    ]
    
    return commits

def save_ndjson(data, filename):
    """Save data as newline-delimited JSON."""
    with open(filename, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def save_bulk_format(data, filename, index_name):
    """Save data in Elasticsearch bulk API format."""
    with open(filename, 'w') as f:
        for item in data:
            f.write(json.dumps({"index": {}}) + '\n')
            f.write(json.dumps(item) + '\n')

if __name__ == "__main__":
    print("=" * 60)
    print("SRE Agent Sample Data Generator")
    print("=" * 60)
    
    # Generate data
    logs = generate_logs()
    commits = generate_commits()
    
    # Save as NDJSON
    save_ndjson(logs, "logs.ndjson")
    save_ndjson(commits, "commits.ndjson")
    
    # Save as Bulk API format
    save_bulk_format(logs, "logs_bulk.json", "application-logs")
    save_bulk_format(commits, "commits_bulk.json", "github-commits")
    
    print(f"\nGenerated {len(logs)} logs ({sum(1 for l in logs if l['level']=='ERROR')} errors)")
    print(f"Generated {len(commits)} commits")
    print(f"\nFiles created:")
    print(f"   - logs.ndjson / logs_bulk.json")
    print(f"   - commits.ndjson / commits_bulk.json")
    print(f"\nBAD COMMIT: f9ed964 by devdave")
    print(f"   'Refactored PaymentProcessor to remove legacy null safety checks'")
    print("=" * 60)
