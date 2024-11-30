from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
from prompt import system_prompt

# Load environment variables
load_dotenv()

# Initialize Flask and OpenAI
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://localhost:5000", "https://framer.com", "*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"]
    }
})
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Add a test route for the root URL
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Essay Generator API is running!",      
        "usage": "Send POST request to /generate-essay"      
    })

@app.route('/generate-essay', methods=['POST'])
def generate_essay():
    try:
        # Get data from request
        data = request.json
        topic = data.get('topic')
        word_count = data.get('wordCount')
        reference_style = data.get('referenceStyle')
        essay_type = data.get('essayType')
        writing_style = data.get('writingStyle')
        tone = data.get('tone')

        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""Please write an essay with the following specifications:
                    Topic: {topic}
                    Word Count: {word_count}
                    Reference Style: {reference_style}
                    Essay Type: {essay_type}
                    Writing Style: {writing_style}
                    Tone: {tone}
                """}
            ],
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.16,
            presence_penalty=0.86
        )
        
        return jsonify({
            "success": True,
            "essay": response.choices[0].message.content
        })

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/test-post', methods=['POST'])
def test_post():
    try:
        data = request.json
        
        # Test OpenAI API call with GPT-4-0
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",  # Using the GPT-4-0 preview model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello!"}
            ],
            max_tokens=100
        )

        return jsonify({
            "success": True,
            "received_data": data,
            "ai_response": response.choices[0].message.content
        })
    except Exception as e:
        print(f"Error in test route: {str(e)}")  # Debug print
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("\nAPI is running!")
    print("=" * 50)
    print("Test the API at: http://localhost:5000")
    print("Generate essays at: http://localhost:5000/generate-essay (POST request)")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)

