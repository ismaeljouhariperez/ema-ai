#!/usr/bin/env python3
"""
Script to test error handling in the EMA-AI API
"""

import requests
import json
import sys
from colorama import init, Fore, Style

# Initialize colorama
init()

# Base URL
base_url = "http://localhost:8000"

def print_response(response):
    """Print a formatted response"""
    print(f"{Fore.BLUE}Status Code: {response.status_code}{Style.RESET_ALL}")
    try:
        data = response.json()
        print(f"{Fore.GREEN}Response:{Style.RESET_ALL}")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(f"{Fore.RED}Failed to parse JSON response:{Style.RESET_ALL}")
        print(response.text)
    print("-" * 50)

def test_invalid_prompt():
    """Test invalid prompt error"""
    print(f"{Fore.YELLOW}Testing invalid prompt error...{Style.RESET_ALL}")
    response = requests.post(f"{base_url}/api/generate", json={"prompt": ""})
    print_response(response)

def test_adventure_not_found():
    """Test adventure not found error"""
    print(f"{Fore.YELLOW}Testing adventure not found error...{Style.RESET_ALL}")
    response = requests.post(f"{base_url}/api/search_similar", json={"adventure_id": 999})
    print_response(response)

def test_health():
    """Test health endpoint"""
    print(f"{Fore.YELLOW}Testing health endpoint...{Style.RESET_ALL}")
    response = requests.get(f"{base_url}/health")
    print_response(response)

def main():
    """Main function"""
    print(f"{Fore.CYAN}EMA-AI API Error Testing{Style.RESET_ALL}")
    print(f"{Fore.CYAN}======================={Style.RESET_ALL}")
    
    # Check if API is running
    try:
        response = requests.get(f"{base_url}/health", timeout=2)
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}Error: Cannot connect to the API at {base_url}{Style.RESET_ALL}")
        print(f"{Fore.RED}Make sure the API is running before running this script.{Style.RESET_ALL}")
        sys.exit(1)
    
    # Run tests
    test_health()
    test_invalid_prompt()
    test_adventure_not_found()
    
    print(f"{Fore.CYAN}All tests completed.{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 