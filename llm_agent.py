from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_visual_json(concept, image_url):
    prompt = f"""
    You are a professional visual design AI.
    The user provided a concept: "{concept}".
    And the product image: {image_url}.
    Create the best possible JSON blueprint for FIBO visual generation.
    Return ONLY valid JSON, with no explanation.PermissionError
    
    JSON structure MUST follow:
    {{
        "camera": {{
            "angle": "",
            "shot_type": "",
            "fov": 0
        }},
        "lighting": {{
            "style": "",
            "intensity": 0.0
        }},
        "composition": {{
            "rule_of_thirds": true,
            "subject_position": ""
        }},
        "color_palette": {{
            "primary": "",
            "secondary": ""
        }},
        "style": {{
            "genre": "",
            "texture": ""
        }}
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    
    return response.choices[0].message.content