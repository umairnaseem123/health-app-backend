"""
Standard, consistent JSON response envelope used across all API endpoints.

Shape:
{
    "success": true,
    "message": "Human readable message",
    "data": { ... } | [ ... ] | null
}
"""
from typing import Any, Optional


def success_response(message: str = "Success", data: Any = None) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message: str = "Something went wrong", data: Any = None) -> dict:
    return {
        "success": False,
        "message": message,
        "data": data,
    }
