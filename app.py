import openai
import time
from flask import Flask, render_template, request

openai.api_key = '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'


app = Flask(__name__)

def generate_story(topic):
    prompt = f"write a story in under 500 words about {topic}"
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def generate_funny_story(story):
    prompt = f"rewrite this story in a funny way: {story}"
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        topic = request.form['topic']
        retry_attempts = 3
        timeout = 10
        original_story = None
        funny_story = None

        while retry_attempts > 0:
            try:
                original_story = generate_story(topic)
                break
            except openai.error.ApiError as e:
                print(f"Error: {e}")
                retry_attempts -= 1
                time.sleep(timeout)

        if original_story:
            retry_attempts = 3

            while retry_attempts > 0:
                try:
                    funny_story = generate_funny_story(original_story)
                    break
                except openai.error.ApiError as e:

                    print(f"Error: {e}")
                    retry_attempts -= 1
                    time.sleep(timeout)

        return render_template('result.html', topic=topic, original_story=original_story, funny_story=funny_story)
    else:
        return render_template('form.html')

if __name__ == '__main__':
    app.run()