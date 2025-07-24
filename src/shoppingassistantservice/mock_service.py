#!/usr/bin/env python3
"""
Mock Shopping Assistant Service for Local Development
Provides realistic responses without requiring Google Cloud services
"""

import json
import random
from flask import Flask, request, jsonify

# Mock product recommendations with realistic product IDs
MOCK_PRODUCTS = [
    {
        "id": "OLJCESPC7Z",
        "name": "Sunglasses",
        "description": "Add a stylish touch to your look with these trendy sunglasses"
    },
    {
        "id": "66VCHSJNUP", 
        "name": "Tank Top",
        "description": "Comfortable and breathable tank top perfect for casual wear"
    },
    {
        "id": "1YMWWN1N4O",
        "name": "Watch",
        "description": "Elegant timepiece that complements any outfit"
    },
    {
        "id": "L9ECAV7KIM",
        "name": "Loafers", 
        "description": "Classic loafers for a sophisticated look"
    },
    {
        "id": "2ZYFJ3GM2N",
        "name": "Keyboard",
        "description": "High-quality mechanical keyboard for your workspace"
    },
    {
        "id": "0PUK6V6EV0",
        "name": "Candle Set",
        "description": "Aromatic candles to create a cozy atmosphere"
    },
    {
        "id": "LS4PSXUNUM",
        "name": "Salt & Pepper Shakers",
        "description": "Stylish seasoning set for your dining table"
    },
    {
        "id": "9SIQT8TOJO",
        "name": "Bamboo Glass Jar",
        "description": "Eco-friendly storage solution for your kitchen"
    },
    {
        "id": "6E92ZMYYFZ",
        "name": "Mug",
        "description": "Perfect coffee mug to start your day right"
    }
]

STYLE_RESPONSES = [
    "modern minimalist with clean lines and neutral colors",
    "cozy rustic with warm wood tones and natural textures", 
    "contemporary industrial with metal accents and exposed elements",
    "classic traditional with elegant furnishings and rich colors",
    "bright scandinavian with light woods and airy feel",
    "sophisticated mid-century modern with vintage appeal"
]

def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['POST'])
    def mock_assistant():
        """Mock AI assistant that provides realistic product recommendations"""
        try:
            data = request.get_json()
            
            # Extract user message
            user_message = data.get('message', 'Help me decorate my room')
            
            # Mock room style analysis
            room_style = random.choice(STYLE_RESPONSES)
            
            # Select 3 random products for recommendation
            recommended_products = random.sample(MOCK_PRODUCTS, 3)
            
            # Generate mock AI response
            response_content = f"""Based on the image you've shared, I can see you have a beautiful {room_style} space. 

For your request: "{user_message}", I'd recommend these items from our catalog:

1. **{recommended_products[0]['name']}** - {recommended_products[0]['description']}

2. **{recommended_products[1]['name']}** - {recommended_products[1]['description']} 

3. **{recommended_products[2]['name']}** - {recommended_products[2]['description']}

These items would complement your room's aesthetic perfectly and help achieve the look you're going for.

[{recommended_products[0]['id']}], [{recommended_products[1]['id']}], [{recommended_products[2]['id']}]"""

            return jsonify({
                'content': response_content
            })
            
        except Exception as e:
            # Fallback response
            fallback_products = MOCK_PRODUCTS[:3]
            return jsonify({
                'content': f"""I'd be happy to help with your decorating needs! Here are some great items I recommend:

1. **{fallback_products[0]['name']}** - {fallback_products[0]['description']}
2. **{fallback_products[1]['name']}** - {fallback_products[1]['description']}
3. **{fallback_products[2]['name']}** - {fallback_products[2]['description']}

[{fallback_products[0]['id']}], [{fallback_products[1]['id']}], [{fallback_products[2]['id']}]"""
            })

    @app.route("/health", methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "mock-shopping-assistant"})

    return app

if __name__ == "__main__":
    print("🤖 Starting Mock Shopping Assistant Service")
    print("🎯 Providing AI-like responses without cloud dependencies")
    print("🌐 Available at http://localhost:8080")
    
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=False)
