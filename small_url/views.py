from flask import flash, redirect, render_template, url_for

from . import app
from .constants import READDRESING_FUNCTION
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short=url_for(
                READDRESING_FUNCTION,
                _external=True,
                short=URLMap.create(
                    original=form.original_link.data,
                    short=form.custom_id.data,
                    need_validate=False
                ).short
            )
        )
    except ValueError as error:
        flash(error)


@app.route('/<string:short>')
def readdressing(short):
    return redirect(URLMap.get_or_404(short=short).original)
