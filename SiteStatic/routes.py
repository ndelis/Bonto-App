from flask import render_template, request
from jinja2 import TemplateNotFound

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)

def calculate_best_rate():
    # Query the Rate table and order by value in ascending order
    best_rate = Rate.query.order_by(Rate.value).first()

    # Return the value of the best rate
    return best_rate.value if best_rate else None

@app.route('/index', methods = ['GET'])
def index():
    best_rate = calculate_best_rate()    
    return render_template('index.html', best_rate=best_rate)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
