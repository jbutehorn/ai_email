import requests
import os
import openai

openai.api_key = os.getenv('OPENAI_KEY')
klaviyo_key = os.getenv('KLAVIYO_KEY')

# Gets AI generated HTML Template
def openai_generate_html_string(brand):
    messages = [
            {
                "role": "user", 
                "content": "Provide an HTML template for an email campaign for " + brand + ". Respond with only an HTML template."
            },
            # {
            #     "role": "system", 
            #     "content": "Response should be in the form of a string that is JSON-escaped." 
            # }, 
            # {
            #     "role": "system",
            #     "content": "Your text output will be directly used in a value for an API call unedited, therefore only respond with a string."
            # }
        ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    print("\n\nOPENAI RESPONSE\n\n")
    print(response)

    return response["choices"][0]["message"]["content"]


# Klaviyo Creates a Template
def create_template(html_template_string):
    url = "https://a.klaviyo.com/api/templates"
 
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Klaviyo-API-Key " + klaviyo_key,
        "Revision": "2023-02-22",
        "Accept": "application/json"
    }
    
    data = {
        "data": {
            "attributes" : {
                "editor_type": "CODE",
                "html": html_template_string,
                "name": "Python Script Test",
                "text": "hello world"
            },
            "type": "template"
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    print("\n\nKLAVIYO CREATE TEMPLATE\n\n")
    print(response_data)

    return response_data["data"]["id"]
    


# Klaviyo Creates a Campaign
def create_campaign():
    url = "https://a.klaviyo.com/api/campaigns"
 
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Klaviyo-API-Key " + klaviyo_key,
        "Revision": "2023-02-22",
        "Accept": "application/json"
    }
    
    data = {
        "data": {
            "type": "campaign",
            "attributes": {
                "name": "Python Test",
                "channel": "email",
                "audiences": {
                    "included": [
                        "SPimPP"
                    ]
                },
                "send_options": {
                    "use_smart_sending": False
                },
                "send_strategy": {
                    "method": "static",
                    "options_static": {
                        "datetime": "2023-08-26T01:04:00.000Z",
                        "is_local": True,
                        "send_past_recipients_immediately": False
                    }
                },
                "tracking_options": {}
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    print("\n\nKLAVIYO CREATE CAMPAIGN\n\n")
    print(response_data)

    return response_data["data"]["attributes"]["message"]

# Klaviyo Assign a Template to a Campaign
def assign_template_to_campaign(template_id, message_id):
    url = "https://a.klaviyo.com/api/campaign-message-assign-template"
 
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Klaviyo-API-Key " + klaviyo_key,
        "Revision": "2023-02-22",
        "Accept": "application/json"
    }
    
    data = {
        "data": {
            "type": "campaign-message",
            "attributes": {
                "template_id": template_id,
                "id": message_id
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    print("\n\nKLAVIYO ASSIGN TEMPLATE\n\n")
    print(response_data)

    print(response.json())




html_template_string = openai_generate_html_string(brand="Company XYZ")
template_id = create_template(html_template_string=html_template_string)

message_id = create_campaign()

assign_template_to_campaign(template_id=template_id, message_id=message_id)

