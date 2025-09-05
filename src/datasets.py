EVALUATION_DATASET = [
    {
        "input": "Find all premium users and notify them about a new feature",
        "expected": {
            "tools_used": ["search_users", "notify_customer"],
            "emails_sent": ["john@example.com"],
            "required_phrases": ["premium", "pro", "new feature"],
        },
        "metadata": {
            "category": "multi-step",
            "difficulty": "medium",
        },
    },
    {
        "input": "Check if john@example.com is an active subscriber",
        "expected": {
            "tools_used": ["get_user_details"],
            "required_phrases": ["John Doe", "pro", "active"],
        },
        "metadata": {
            "category": "single-lookup",
            "difficulty": "easy",
        },
    },
    {
        "input": "Find expired subscriptions and send them renewal reminders",
        "expected": {
            "tools_used": ["search_users", "notify_customer"],
            "subscription_status": "expired",
            "emails_sent": ["user@example.com"],
        },
        "metadata": {
            "category": "multi-step",
            "difficulty": "medium",
        },
    },
    {
        "input": "Cancel the subscription for john@example.com",
        "expected": {
            "tools_used": ["update_subscription"],
            "subscriptions_updated": ["john@example.com"],
            "action": "cancel",
        },
        "metadata": {
            "category": "single-action",
            "difficulty": "easy",
        },
    },
    {
        "input": "Upgrade user123 to enterprise plan",
        "expected": {
            "tools_used": ["update_subscription"],
            "subscriptions_updated": ["user123"],
            "action": "upgrade",
            "new_plan": "enterprise",
        },
        "metadata": {
            "category": "single-action",
            "difficulty": "easy",
        },
    },
]
