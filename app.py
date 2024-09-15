from flask import Flask, render_template, request
import os
from ImageCreator import ImageCreator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
image_creator = ImageCreator()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    image = request.files['image']
    to_memorize = request.form['prompt']
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.png'))
    generated_image_url = image_creator.create_image(to_memorize, os.path.join(app.config['UPLOAD_FOLDER'], 'image.png'))
    print(generated_image_url)
    return render_template('generate.html', image_url=generated_image_url)

if __name__ == '__main__':
    app.run()