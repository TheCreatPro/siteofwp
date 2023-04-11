import flask

from . import db_session
from .news import News

blueprint = flask.Blueprint('news_api', __name__, template_folder='templates')


# @blueprint.route('/api/news')
# def get_all_news():
#     db_sess = db_session.create_session()
#     news = db_sess.query(News).all()
#     return flask.jsonify(
#         {
#             'jobs':
#                 [item.to_dict(only=('title', 'content', 'user.name')) for item
#                  in news]
#         }
#     )


# @blueprint.route('/api/news/<job_id>')
# def get_news(job_id):
#     if not job_id.isdigit():
#         return flask.jsonify({'ERROR': 'Введите число!'})
#     db_sess = db_session.create_session()
#     news = db_sess.query(News).get(int(job_id))
#     if news:
#         return flask.jsonify(
#             {
#                 'news': news.to_dict(only=('title', 'content', 'user.name'))
#             }
#         )
#     else:
#         return flask.jsonify({'ERROR': 'Ошибка в запросе!'})


# @blueprint.route('/api/news', methods=['POST'])
# def create_news():
#     if not flask.request.json:
#         return flask.jsonify({'error': 'Empty request'})
#     elif not all(key in flask.request.json for key in
#                  ['id', 'title', 'content', 'user_id', 'is_private']):
#         return flask.jsonify({'error': 'Bad request'})
#     db_sess = db_session.create_session()
#     num = int(flask.request.json['id'])
#     # проверяем, есть ли этот id у нас в БД:
#     rpt = db_sess.query(News).filter(News.id == num).first()
#     if rpt:
#         return flask.jsonify({'error': 'the id already exists'})
#     news = News(
#         title=flask.request.json['title'],
#         content=flask.request.json['content'],
#         user_id=flask.request.json['user_id'],
#         is_private=flask.request.json['is_private']
#     )
#     db_sess.add(news)
#     db_sess.commit()
#     return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/news/<news_id>', methods=['DELETE'])
def delete_news(news_id):
    if not news_id.isdigit():
        return flask.jsonify({'ERROR': 'Введите число!'})
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(int(news_id))
    if news:
        db_sess.delete(news)
        db_sess.commit()
        return flask.jsonify({'success': 'Работа удалена'})
    else:
        return flask.jsonify({'ERROR': 'Ошибка в запросе!'})
