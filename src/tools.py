from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypedDict


class ToolResult(TypedDict):
    """Result from a tool execution"""

    success: bool
    message: str
    data: Optional[Dict[str, Any]]


class Tool(ABC):
    """Abstract base class for agent tools"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name for LLM function calling"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for LLM function calling"""
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """Tool parameters schema for LLM function calling"""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters"""
        pass

    def to_function_schema(self) -> Dict[str, Any]:
        """Convert tool to OpenAI function calling schema"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class NotifyCustomerTool(Tool):
    """Purpose-built tool for sending customer notifications"""

    @property
    def name(self) -> str:
        return "notify_customer"

    @property
    def description(self) -> str:
        return "Send a notification to a customer about their account or service"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The customer's user ID"},
                "message": {
                    "type": "string",
                    "description": "The notification message to send",
                },
                "notification_type": {
                    "type": "string",
                    "enum": ["email", "sms", "push"],
                    "description": "Type of notification to send",
                },
            },
            "required": ["user_id", "message", "notification_type"],
        }

    async def execute(
        self, user_id: str, message: str, notification_type: str
    ) -> ToolResult:
        # In a real implementation, this would integrate with your notification service
        try:
            # Simulate sending notification
            print(f"Sending {notification_type} to user {user_id}: {message}")

            return {
                "success": True,
                "message": f"Successfully sent {notification_type} notification to user {user_id}",
                "data": {
                    "user_id": user_id,
                    "notification_type": notification_type,
                    "sent_at": "2024-01-15T10:30:00Z",
                },
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to send notification: {str(e)}",
                "data": None,
            }


class SearchUsersTool(Tool):
    """Purpose-built tool for searching users with business-relevant filters"""

    @property
    def name(self) -> str:
        return "search_users"

    @property
    def description(self) -> str:
        return "Search for users using business-relevant criteria like subscription status or account type"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Search by email address"},
                "subscription_status": {
                    "type": "string",
                    "enum": ["active", "cancelled", "expired", "trial"],
                    "description": "Filter by subscription status",
                },
                "account_type": {
                    "type": "string",
                    "enum": ["free", "pro", "enterprise"],
                    "description": "Filter by account type",
                },
            },
        }

    async def execute(
        self,
        email: Optional[str] = None,
        subscription_status: Optional[str] = None,
        account_type: Optional[str] = None,
    ) -> ToolResult:
        # In a real implementation, this would query your user database
        try:
            # Simulate user search
            mock_users = [
                {
                    "user_id": "user_123",
                    "email": email or "john@example.com",
                    "subscription_status": subscription_status or "active",
                    "account_type": account_type or "pro",
                }
            ]

            return {
                "success": True,
                "message": f"Found {len(mock_users)} user(s) matching criteria",
                "data": {"users": mock_users, "total_count": len(mock_users)},
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to search users: {str(e)}",
                "data": None,
            }


class GetUserDetailsTool(Tool):
    """Purpose-built tool for getting comprehensive user information"""

    @property
    def name(self) -> str:
        return "get_user_details"

    @property
    def description(self) -> str:
        return "Get detailed information about a specific user including account status and history"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's unique identifier",
                }
            },
            "required": ["user_id"],
        }

    async def execute(self, user_id: str) -> ToolResult:
        # In a real implementation, this would query your user database
        try:
            # Simulate user lookup
            mock_user_details = {
                "user_id": user_id,
                "email": "john@example.com",
                "name": "John Doe",
                "subscription_status": "active",
                "account_type": "pro",
                "created_at": "2023-01-15T10:30:00Z",
                "last_login": "2024-01-14T15:45:00Z",
                "billing_info": {
                    "next_billing_date": "2024-02-15T00:00:00Z",
                    "amount": "$29.99",
                },
            }

            return {
                "success": True,
                "message": f"Retrieved details for user {user_id}",
                "data": {"user": mock_user_details},
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get user details: {str(e)}",
                "data": None,
            }


class UpdateSubscriptionTool(Tool):
    """Purpose-built tool for handling subscription changes"""

    @property
    def name(self) -> str:
        return "update_subscription"

    @property
    def description(self) -> str:
        return "Update a user's subscription plan or status"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's unique identifier",
                },
                "action": {
                    "type": "string",
                    "enum": ["upgrade", "downgrade", "cancel", "reactivate"],
                    "description": "The subscription action to perform",
                },
                "new_plan": {
                    "type": "string",
                    "enum": ["free", "pro", "enterprise"],
                    "description": "The new subscription plan (required for upgrade/downgrade)",
                },
            },
            "required": ["user_id", "action"],
        }

    async def execute(
        self, user_id: str, action: str, new_plan: Optional[str] = None
    ) -> ToolResult:
        # In a real implementation, this would integrate with your billing system
        try:
            # Simulate subscription update
            result_message = f"Successfully performed {action} for user {user_id}"
            if new_plan:
                result_message += f" to {new_plan} plan"

            return {
                "success": True,
                "message": result_message,
                "data": {
                    "user_id": user_id,
                    "action": action,
                    "new_plan": new_plan,
                    "effective_date": "2024-01-15T10:30:00Z",
                },
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update subscription: {str(e)}",
                "data": None,
            }


def get_tools() -> list[Tool]:
    return [
        NotifyCustomerTool(),
        SearchUsersTool(),
        GetUserDetailsTool(),
        UpdateSubscriptionTool(),
    ]
