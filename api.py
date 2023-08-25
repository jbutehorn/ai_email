from flask import Flask, json
import app

api = Flask(__name__)

@api.route('/create_campaign', methods=['POST'])
def create_campaign():
    app.openai_generate_html_string("Test Brand")

if __name__ == '__main__':
    api.run()