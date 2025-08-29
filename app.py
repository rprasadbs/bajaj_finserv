from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Fixed user details
FIXED_USER_ID = "john_doe_17091999"
FIXED_EMAIL = "john@xyz.com"
FIXED_ROLL_NUMBER = "ABCD123"

def process_data(data_array):
    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []
    alpha_for_concat = []
    total_sum = 0

    if not isinstance(data_array, list):
        return [], [], [], [], "0", "", False, "Input 'data' must be an array."

    for item in data_array:
        if not isinstance(item, str):
            continue

        # Numbers
        if item.isdigit():
            num = int(item)
            if num % 2 == 0:
                even_numbers.append(item)
            else:
                odd_numbers.append(item)
            total_sum += num

        # Alphabets (whole words)
        elif item.isalpha():
            alphabets.append(item.upper())
            alpha_for_concat.extend(list(item))  # preserve original case for alternating caps

        # Special characters
        else:
            special_characters.append(item)

    # Build alternating caps reversed string
    reversed_alpha = list("".join(alpha_for_concat))[::-1]
    concat_chars = []
    for i, ch in enumerate(reversed_alpha):
        concat_chars.append(ch.upper() if i % 2 == 0 else ch.lower())
    concat_string = "".join(concat_chars)

    return odd_numbers, even_numbers, alphabets, special_characters, str(total_sum), concat_string, True, None


# ✅ Health check / root route (so opening base URL doesn't give 404)
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Server is running 🚀. Use POST /bfhl with JSON data."
    })


# ✅ POST /bfhl route
@app.route('/bfhl', methods=['POST'])
def bfhl():
    try:
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
        if input_array is None:
            return jsonify({
                "is_success": False,
                "user_id": FIXED_USER_ID,
                "email": FIXED_EMAIL,
                "roll_number": FIXED_ROLL_NUMBER,
                "error": "Missing 'data' array in request body."
            }), 400

        odd_numbers, even_numbers, alphabets, special_characters, total_sum_str, concat_string, is_success, error_message = process_data(input_array)

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

        if not is_success:
            response_payload["error"] = error_message
            return jsonify(response_payload), 400

        return jsonify(response_payload), 200

    except Exception as e:
        return jsonify({
            "is_success": False,
            "user_id": FIXED_USER_ID,
            "email": FIXED_EMAIL,
            "roll_number": FIXED_ROLL_NUMBER,
            "error": f"Unexpected error: {str(e)}"
        }), 500


# ✅ GET /bfhl route
@app.route('/bfhl', methods=['GET'])
def bfhl_get():
    return jsonify({"operation_code": 1})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # use hosting port if available
    app.run(debug=True, host='0.0.0.0', port=port)
