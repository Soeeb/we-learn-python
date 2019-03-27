from flask import Flask, render_template, request
import math
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
class Image:
        def __init__(self, filename, title):
            self.filename = filename
            self.title = title  
            self.rating = []


        def rating_append(self, rating):
            self.rating.append(rating)

        def rating_average(self):
            return round(math.fsum(self.rating)/len(self.rating),2)

images = []
import os
path = os.getcwd()+"/static/images"
for filename in os.listdir(path):
    images.append(Image(filename, "Savage Chickens, Doug Savage"))

@app.route('/')
def main():
    
    return render_template("index.html", images = images)

@app.route('/rate', methods =["POST","GET"])
def mainRate():
    rating = None
    if request.method == "POST":
        form = request.form
        filename = request.args.get("imageName")
        for image in images:
            if image.filename == filename:
                rate_value = int(form["rating"])
                image.rating_append(rate_value)
                rating = image.rating_average()
                print(rating)
    return render_template("rate.html", rating = rating)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug = True)
