from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Course, Comment
from transformers import pipeline
# Initialize the sentiment analysis and keyword extraction pipelines
sentiment_analysis_pipeline = pipeline('sentiment-analysis')
keyword_extraction_pipeline = pipeline('ner')  # Named Entity Recognition can be used for keyword extraction

def perform_sentiment_analysis(text):
    return sentiment_analysis_pipeline(text)

def extract_keywords(text):
    entities = keyword_extraction_pipeline(text)
    return [entity['word'] for entity in entities]

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/course/<int:course_id>/report', methods=['GET'])
@jwt_required()
def generate_course_report(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404

    comments = Comment.query.filter_by(course_id=course_id).all()
    total_comments = len(comments)
    total_likes = sum(comment.likes for comment in comments)

    return jsonify({
        'course_name': course.name,
        'total_comments': total_comments,
        'total_likes': total_likes,
    })

@analysis_bp.route('/comments/<int:comment_id>/analyze', methods=['POST'])
@jwt_required()
def analyze_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    analysis_type = request.json.get('type', 'sentiment')  # 'sentiment' 或 'keywords'
    result = None

    if analysis_type == 'sentiment':
        result = perform_sentiment_analysis(comment.content)
    elif analysis_type == 'keywords':
        result = extract_keywords(comment.content)
    else:
        return jsonify({'message': 'Invalid analysis type'}), 400

    return jsonify({'analysis_result': result})
