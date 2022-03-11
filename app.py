from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

PERSONS = {
    'person1': {'name': 'Mario', 'surname': 'Doman', 'height': 198, 'age': 40},
    'person2': {'name': 'Palo', 'surname': 'Fritz', 'height': 189, 'age': 25},
    'person3': {'name': 'Peto', 'surname': 'Hans', 'height': 176, 'age': 17},
}


def abort_if_person_doesnt_exist(person_id):
    if person_id not in PERSONS:
        abort(404, message=f"{person_id} doesn't exist")

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('surname')
parser.add_argument('height')
parser.add_argument('age')



# shows single person, delete person, update person
class Person(Resource):
    def get(self, person_id):        
        abort_if_person_doesnt_exist(person_id)        
        return PERSONS[person_id]

    def delete(self, person_id):
        abort_if_person_doesnt_exist(person_id)
        del PERSONS[person_id]
        return 204

    def put(self, person_id):
        args = parser.parse_args()
        person = {'name': args['name'], 
                            'surname': args['surname'],
                            'height': int(args['height']),
                            'age': int(args['age'])}
        PERSONS[person_id] = person
        return person, 201



# list of all persons, POST new person
class PersonList(Resource):
    def get(self):
        return PERSONS

    def post(self):
        args = parser.parse_args()
        person_id = int(max(PERSONS.keys()).lstrip('person')) + 1
        person_id = f'person{person_id}'
        PERSONS[person_id] = {'name': args['name'], 
                            'surname': args['surname'],
                            'height': int(args['height']),
                            'age': int(args['age'])}

        return PERSONS[person_id], 201


# routing
api.add_resource(PersonList, '/persons')
api.add_resource(Person, '/persons/<person_id>')


if __name__ == '__main__':
    app.run(debug=True)