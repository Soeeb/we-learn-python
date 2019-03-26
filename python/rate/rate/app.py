from flask import Flask, request, render_template
app = Flask(__name__)

class Image():

	def __init__ (self, filename,credit):
		self.filename = filename
		self.credit = credit
		self.rating = []

	def add_rating(self, input):
		self.rating.append(input)

	def average_rating(self):
		result = 0
		sum = 0
		for rating in self.rating:
			sum += rating
		result = sum / len(self.rating)
		return result




images = []
import os
path = os.getcwd()+"/static/images"
for filename in os.listdir(path):
	#create image object and add to images list
	images.append(Image(filename, "Savage Chickens, Doug Savage"))
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app



@app.route('/', methods = ["GET", "POST"])
def hello():

    """Renders a sample page."""
    return render_template('index.html', images = images)

@app.route('/rate', methods = ["GET", "POST"])
def rate():
	average = None
	if request.method == "POST":
		filename = request.args.get("imageName")
		form = request.form
		rating = int(form["rate"])
		for image in images:
			if image.filename == filename:
				image.rating.append(rating)
				average = image.average_rating()
				return render_template('rate.html', average = f"The Average rating for this image is: {average} Stars")
		

	return render_template('rate.html', average = "None")

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug = True)
