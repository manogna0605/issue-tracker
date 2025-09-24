from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

issues = []
issue_id_counter = 1

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/issues', methods=['GET'])
def get_issues():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 5))
    status = request.args.get('status')
    priority = request.args.get('priority')
    assignee = request.args.get('assignee')

    result = issues
    if status:
        result = [i for i in result if i['status'] == status]
    if priority:
        result = [i for i in result if i['priority'] == priority]
    if assignee:
        result = [i for i in result if i['assignee'] == assignee]

    start = (page - 1) * page_size
    end = start + page_size
    return jsonify(result[start:end])

@app.route('/issues/<int:uid>', methods=['GET'])
def get_issue(uid):
    for issue in issues:
        if issue['id'] == uid:
            return jsonify(issue)
    return jsonify({'error': 'Not found'}), 404

@app.route('/issues', methods=['POST'])
def create_issue():
    global issue_id_counter
    data = request.json
    new_issue = {
        'id': issue_id_counter,
        'title': data['title'],
        'status': data.get('status', 'Open'),
        'priority': data.get('priority', 'Low'),
        'assignee': data.get('assignee', ''),
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    issues.append(new_issue)
    issue_id_counter += 1
    return jsonify(new_issue), 201

@app.route('/issues/<int:uid>', methods=['POST'])
def update_issue(uid):
    data = request.json
    for issue in issues:
        if issue['id'] == uid:
            issue.update(data)
            issue['updatedAt'] = datetime.now().isoformat()
            return jsonify(issue)
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)


    @app.route('/')
    def index():
        return "Flask server is running"