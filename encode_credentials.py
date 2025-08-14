#!/usr/bin/env python3
"""
Helper script to base64 encode Google Cloud credentials for deployment
"""

import base64
import sys
import json

def encode_credentials(json_file_path):
    """
    Encode Google Cloud service account JSON file to base64
    for use in environment variables during deployment
    """
    try:
        with open(json_file_path, 'r') as file:
            # Read and validate JSON
            json_content = json.load(file)
            
            # Convert back to string for encoding
            json_string = json.dumps(json_content)
            
            # Encode to base64
            encoded = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')
            
            print("✅ Successfully encoded Google Cloud credentials!")
            print("\nFor Render deployment, set this as your GOOGLE_APPLICATION_CREDENTIALS environment variable:")
            print("-" * 80)
            print(encoded)
            print("-" * 80)
            print("\nNote: Keep this value secure and don't share it publicly!")
            
            return encoded
            
    except FileNotFoundError:
        print(f"❌ Error: File '{json_file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"❌ Error: '{json_file_path}' is not a valid JSON file.")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python encode_credentials.py <path_to_google_cloud_key.json>")
        print("Example: python encode_credentials.py google-cloud-key.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    encode_credentials(json_file)
