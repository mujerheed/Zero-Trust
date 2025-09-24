import json
import os
import string
import secrets
import boto3
from datetime import datetime, timedelta

# Initialize the DynamoDB client
# The boto3 library automatically picks up credentials from the configured AWS CLI.
dynamodb = boto3.resource('dynamodb')

# Retrieve the DynamoDB table name from an environment variable for security and flexibility.
# This avoids hardcoding the table name in the code.
try:
    OTP_TABLE_NAME = os.environ['OTP_TABLE_NAME']
    otp_table = dynamodb.Table(OTP_TABLE_NAME)
except KeyError:
    print("Error: OTP_TABLE_NAME environment variable not set.")
    # In a real-world scenario, you would handle this error more gracefully,
    # but for this project, a clear message is sufficient.
    raise Exception("OTP_TABLE_NAME environment variable must be set.")

def generate_otp(length=8, use_special_chars=False):
    """
    Generates a cryptographically secure, random alphanumeric OTP.

    Args:
        length (int): The desired length of the OTP.
        use_special_chars (bool): If True, includes a set of special characters
                                   to increase complexity for CEO/Admin OTPs.

    Returns:
        str: A randomly generated OTP.
    """
    # Define the character set for the OTP.
    # The 'secrets' module is used for cryptographic purposes, making it more secure than 'random'.
    characters = string.ascii_letters + string.digits
    if use_special_chars:
        # Add a mix of common symbols for higher complexity.
        characters += '!@#$%^&*().:-_+'
        
    # Generate the OTP by selecting random characters from the defined set.
    otp = ''.join(secrets.choice(characters) for _ in range(length))
    return otp

def lambda_handler(event, context):
    """
    AWS Lambda function handler for generating and storing OTPs.

    This function is triggered by an API Gateway request and expects a JSON payload
    with 'identifier' (e.g., phone number, email) and 'user_role' (e.g., 'buyer', 'vendor', 'ceo').
    It generates a unique OTP, stores it in DynamoDB, and returns a success message.

    The DynamoDB entry includes the OTP, the identifier, and an expiration timestamp
    to ensure the OTP is single-use and time-bound.
    """
    print("Received event: " + json.dumps(event, indent=2))
    
    # Extract data from the event body.
    try:
        body = json.loads(event['body'])
        identifier = body['identifier']
        user_role = body['user_role']
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing event body: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request body. Missing "identifier" or "user_role".'})
        }

    # Determine OTP length and complexity based on the user role, as per the proposal.
    if user_role == 'ceo':
        otp_length = 12
        use_special_chars = True
    else:
        otp_length = 8
        use_special_chars = False

    # Generate the OTP and set its expiration timestamp (e.g., 5 minutes from now).
    otp = generate_otp(length=otp_length, use_special_chars=use_special_chars)
    otp_expiry_time = (datetime.utcnow() + timedelta(minutes=5)).isoformat()

    # Store the OTP in DynamoDB.
    try:
        otp_table.put_item(
            Item={
                'identifier': identifier,
                'otp': otp,
                'user_role': user_role,
                'status': 'pending',  # Use 'pending' initially, 'used' after verification.
                'createdAt': datetime.utcnow().isoformat(),
                'expiresAt': otp_expiry_time
            }
        )
        print(f"OTP successfully stored for identifier: {identifier}")
    except Exception as e:
        print(f"Error storing OTP in DynamoDB: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Could not store OTP. Please try again.'})
        }
    
    # Return a success response. The actual OTP is not returned here for security reasons,
    # as it will be sent to the user via SNS/SES in a separate function.
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'OTP generated and stored successfully.'})
    }
