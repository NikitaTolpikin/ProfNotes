from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
import json

with open('config.json') as f:
    settings = json.load(f)

app = Flask(__name__)
api = Api(app)

note_dict = {
    1: {
        'title': 'string',
        'content': 'string'
    }
}

class NoteList(Resource):
    def get(self):
        note_list = [{'id': k, 'content':v['content'], 'title': v['title']} for k, v in note_dict.items()]
        return note_list, 200

    def post(self):
        if note_dict:
            new_note_id = max(note_dict.keys()) + 1
        else:
            new_note_id = 0
        json_data = request.get_json(force=True)
        content = json_data['content']
        if 'title' in json_data:
            title = json_data['title']
        else:
            n_int = settings['N']
            n_int = max(len(content), n_int)
            title = content[:n_int]
        note_dict[new_note_id] = {'title': title, 'content': content}
        note = {'id': new_note_id, 'title': title, 'content': content}
        return note, 200

class Note(Resource):
    def get(self, note_id):
        note_id = int(note_id)
        note = note_dict[note_id]
        return note

    def put(self, note_id):
        note_id = int(note_id)
        note = note_dict[note_id]
        json_data = request.get_json(force=True)
        if 'content' in json_data:
            note['content'] = json_data['content']
        if 'title' in json_data:
            note['title'] = json_data['title']
        return note, 200

    def delete(self, note_id):
        note_id = int(note_id)
        note_dict.pop(note_id)
        return 200

api.add_resource(NoteList, '/notes')
api.add_resource(Note, '/notes/<note_id>')

if __name__ == '__main__':
    app.run(debug=True)