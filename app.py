# Import necessary libraries for building the web application
from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# --- Fixed User Details (as per objective requirement) ---
# These values are hardcoded as per the example provided in the problem description.
# In a real-world scenario, these might come from a user database or authentication system.
FIXED_USER_ID = "john_doe_17091999"
FIXED_EMAIL = "john@xyz.com"
FIXED_ROLL_NUMBER = "ABCD123"

def process_data(data_array):
    """
    Processes the input array to categorize items and perform calculations.

    Args:
        data_array (list): The array of mixed data (strings representing numbers, alphabets, special characters).

    Returns:
        tuple: A tuple containing lists for odd_numbers, even_numbers, alphabets,
               special_characters, the sum as a string, the concatenated string,
               a success status (boolean), and an error message (string or None).
    """
    odd_numbers = []
    even_numbers = []
    alphabets = [] # Stores entire alphabetic strings (e.g., "ABCD")
    special_characters = []
    all_alpha_chars_for_concat = [] # Stores individual alphabet characters for concatenation
    total_sum = 0
    is_success = True
    error_message = None

    # Validate if the input is actually a list
    if not isinstance(data_array, list):
        is_success = False
        error_message = "Input 'data' must be an array."
        # Return initial values in case of an immediate error
        return odd_numbers, even_numbers, alphabets, special_characters, "0", "", is_success, error_message

    # Iterate through each item in the input data array
    for item in data_array:
        # Ensure the item is a string before processing, as per examples
        if not isinstance(item, str):
            continue # Skip non-string items

        # 1. Check if the item is an integer string (e.g., "1", "334")
        if item.isdigit():
            try:
                num = int(item)
                if num % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
                total_sum += num
            except ValueError:
                # This block should ideally not be reached if item.isdigit() is true,
                # but it's a safeguard for robust error handling.
                pass
        # 2. Check if the item consists ONLY of alphabetic characters (e.g., "A", "ABcD", "DOE")
        elif item.isalpha():
            alphabets.append(item.upper()) # Add the entire item (uppercase) to alphabets list
            # Extract individual characters for concatenation
            for char in item:
                all_alpha_chars_for_concat.append(char.upper())
        # 3. If item is neither a pure digit string nor a pure alphabetic string,
        #    it must be a mixed string (e.g., "a1b") or contain special characters (e.g., "$", "&")
        else:
            for char in item:
                if char.isalpha():
                    # Individual alphabetic characters from mixed strings contribute to concatenation
                    all_alpha_chars_for_concat.append(char.upper())
                elif not char.isspace() and not char.isdigit():
                    # Non-alphabetic, non-digit, non-space characters are considered special characters
                    special_characters.append(char)

    # --- Concatenation of alphabetical characters in reverse and alternating caps ---
    concat_string_chars = []
    # Iterate through the collected alphabetical characters in reverse order
    for i, char in enumerate(reversed(all_alpha_chars_for_concat)):
        if i % 2 == 0: # First, third, fifth, etc. character (from reversed list) will be uppercase
            concat_string_chars.append(char.upper())
        else: # Second, fourth, sixth, etc. character (from reversed list) will be lowercase
            concat_string_chars.append(char.lower())
    concat_string = "".join(concat_string_chars) # Join all characters to form the final string

    return odd_numbers, even_numbers, alphabets, special_characters, str(total_sum), concat_string, is_success, error_message

@app.route('/bfhl', methods=['POST'])
def bfhl():
    """
    Handles the POST request to the /bfhl endpoint.
    Expects a JSON body with a 'data' array.
    """
    try:
        # Get the JSON data from the request body
        request_data = request.get_json()
        if request_data is None:
            return jsonify({
                "is_success": False,
                "user_id": FIXED_USER_ID,
                "email": FIXED_EMAIL,
                "roll_number": FIXED_ROLL_NUMBER,
                "error": "Request body must be valid JSON."
            }), 400

        input_array = request_data.get('data')

        # Check if the 'data' array is missing from the request
        if input_array is None:
            return jsonify({
                "is_success": False,
                "user_id": FIXED_USER_ID,
                "email": FIXED_EMAIL,
                "roll_number": FIXED_ROLL_NUMBER,
                "error": "Missing 'data' array in request body."
            }), 400

        # Process the input array using the helper function
        odd_numbers, even_numbers, alphabets, special_characters, total_sum_str, concat_string, is_success, error_message = process_data(input_array)

        # Construct the response payload
        response_payload = {
            "is_success": is_success,
            "user_id": FIXED_USER_ID,
            "email": FIXED_EMAIL,
            "roll_number": FIXED_ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": total_sum_str,
            "concat_string": concat_string
        }

        # If processing was not successful, include the error message and return a 400 status
        if not is_success:
            response_payload["error"] = error_message
            return jsonify(response_payload), 400 # Bad request due to invalid input type

        # Return the successful response with a 200 OK status
        return jsonify(response_payload), 200

    except Exception as e:
        # Catch any unexpected errors during request processing and return a 500 Internal Server Error
        return jsonify({
            "is_success": False,
            "user_id": FIXED_USER_ID,
            "email": FIXED_EMAIL,
            "roll_number": FIXED_ROLL_NUMBER,
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500

# This ensures the Flask development server runs when the script is executed directly
if __name__ == '__main__':
    # debug=True provides helpful error messages during development but should be False in production
    app.run(debug=True, host='0.0.0.0', port=5000)
