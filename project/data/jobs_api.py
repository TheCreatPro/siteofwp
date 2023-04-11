import flask

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


# @blueprint.route('/api/jobs')
# def get_all_news():
#     db_sess = db_session.create_session()
#     jobs = db_sess.query(Jobs).all()
#     return flask.jsonify(
#         {
#             'jobs':
#                 [item.to_dict(only=(
#                     'team_leader', 'job', 'work_size', 'collaborators',
#                     'start_date', 'end_date', 'is_finished')) for item in jobs]
#         }
#     )
#
#
# @blueprint.route('/api/jobs/<int:job_id>')
# def get_news(job_id):
#     if not job_id.isdigit():
#         return flask.jsonify({'ERROR': 'Введите число!'})
#     db_sess = db_session.create_session()
#     jobs = db_sess.query(Jobs).get(int(job_id))
#     if jobs:
#         return flask.jsonify(
#             {
#                 'jobs':
#                     jobs.to_dict(only=(
#                         'team_leader', 'job', 'work_size', 'collaborators',
#                         'start_date', 'end_date', 'is_finished'))
#             }
#         )
#     else:
#         return flask.jsonify({'ERROR': 'Ошибка в запросе!'})


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not flask.request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in flask.request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()

    num = int(flask.request.json['id'])
    # проверяем, есть ли этот id у нас в БД:
    rpt = db_sess.query(Jobs).filter(Jobs.id == num).first()
    if rpt:
        return flask.jsonify({'error': 'the id already exists'})

    jobs = Jobs(
        team_leader=flask.request.json['team_leader'],
        job=flask.request.json['job'],
        work_size=flask.request.json['work_size'],
        collaborators=flask.request.json['collaborators'],
        start_date=flask.request.json['start_date'],
        end_date=flask.request.json['end_date'],
        is_finished=flask.request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    if not job_id.isdigit():
        return flask.jsonify({'ERROR': 'Введите число!'})
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(int(job_id))
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
        return flask.jsonify({'success': 'Работа удалена'})
    else:
        return flask.jsonify({'ERROR': 'Ошибка в запросе!'})