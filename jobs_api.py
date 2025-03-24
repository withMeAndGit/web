from flask import Blueprint, jsonify, Response, make_response, request
from werkzeug import Response
from data import db_session
from data.jobs import Jobs

from sqlalchemy.exc import NoResultFound

JOBS_COLUMNS = list(Jobs.__dict__.keys())[4:]

blueprint = Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs() -> Response:
    session = db_session.create_session()
    jobs_list: list[type[Jobs]] = session.query(Jobs).all()

    return jsonify({
        'jobs': [job.to_dict() for job in jobs_list]
    })


@blueprint.route('/api/jobs/<int:_id>')
def get_job(_id: int) -> Response:
    try:
        session = db_session.create_session()
        jobs_list: type[Jobs] = session.query(Jobs).where(Jobs.id == _id).one()

        return jobs_list.to_dict()
    
    except NoResultFound:
        return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json and all(key in JOBS_COLUMNS for key in request.json):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    session = db_session.create_session()
    jobs: Jobs = Jobs(
        team_leader = request.json.get('team_leader', None),
        job = request.json.get('job', None),
        work_size = request.json.get('work_size', None),
        collaborators = request.json.get('collaborators', None),
        start_date = request.json.get('start_date', None),
        end_date = request.json.get('end_date', None),
        is_finished = request.json.get('is_finished', 0)
        )

    session.add(jobs)
    session.commit()

    return jsonify({})