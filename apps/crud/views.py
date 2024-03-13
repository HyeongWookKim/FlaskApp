from flask import Blueprint, render_template


# Blueprint로 crud 앱 생성
crud = Blueprint(
    'crud',
    __name__,
    template_folder = 'templates',
    static_folder = 'static'
)

@crud.route('/')
def index():
    return render_template('crud/index.html')