import datetime
import json
from flask import Flask, request
from scrape import scrape
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)



class OpenGraphNode(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), unique=True, nullable=True)
    type = db.Column(db.String(120), unique=False, nullable=True)
    title = db.Column(db.String(200), unique=False, nullable=True)
    update_time = db.Column(db.DateTime, unique=False, default=datetime.datetime.utcnow)

    def __init__(self, url, type=None ,title=None):
        self.url = url
        self.type = type
        self.title = title

    def as_dict(self):

        return {
            "url": self.url,
            "type": self.type,
            "title": self.title,
            "image": {
                "url": "http://ogp.me/logo.png",
                "type": "image/png",
                "width": 300,
                "height": 300,
                "alt": "The Open Graph logo"
            },
            "scrape_status" : "done",
            "updated_time": "2018-02-18T03:41:09+0000",
            "id": "10150237978467733"
        }


@app.route('/stories', methods=['GET', 'POST', 'DELETE', 'PUT'])
def post_stories():

    # print(f'args:\n{request.args}\n\n')
    # print(f'data:\n{request.data}\n\n')
    # print(f'headers:\n{request.headers}\n\n')
    # print(f'mimetypes:\n{request.accept_mimetypes}\n\n')
    # print(f'encodings:\n{request.accept_encodings}\n\n')


    print("request method: " + request.method)

    if request.method != 'POST':

        return 'Hello there scraper please use POST!'

    else:

        url = request.args.get('url')

        print(f'did you ask for scraping of:  {url}    ?\n')

        data = {"please add url to params": 7}

        if url is None:

            return json.dumps(data)


        node = scrape(url)

        print(node.as_dict())

        try:

            db.session.add(node)
            db.session.commit()

        except Exception:

            pass


        data = node.as_dict()

        return json.dumps(data)


@app.route('/stories/<canonical_url_id>')
def get_stories(canonical_url_id):


    return f'Hello there {canonical_url_id} scraper!'


@app.route('/<name>')
def hello_name(name):
    return f"Hello {name} world!"




if __name__ == '__main__':

    db.create_all()
    app.run(debug=True, host='0.0.0.0')

