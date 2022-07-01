from flask import Blueprint, jsonify, request
from flask_login import login_required
from backend import db

class CrudBluePrint(Blueprint):

    def __init__(self, name, import_name,  model,  url_prefix=None, **kwargs):
        super().__init__(name, import_name, url_prefix, **kwargs)
        self.model = model
        self.schema = model.get_schema()
        self.register_routes()

    def register_routes(self):
        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/<int:id>', view_func=self.get_item)
        self.add_url_rule('/', view_func=self.create_item, methods=['POST'])
        self.add_url_rule(
            '/<int:id>', view_func=self.update_item, methods=['PUT'])
        self.add_url_rule(
            '/<int:id>', view_func=self.delete_item, methods=['DELETE'])

    @login_required
    def index(self):
        query = self.model.query
        # Iterate through request parameters in URL
        for attr, value in request.args.items():
            # Apply filter if the model's schema has the attribute
            if attr in self.schema.fields:
                if attr.startswith('is_') or attr.endswith('_id') or attr == 'id':
                    query = query.filter(getattr(self.model, attr) == value)
                else:
                    query = query.filter(
                        getattr(self.model, attr).ilike(f'%{value}%'))

        items = query.all()
        return jsonify(self.schema.dump(items, many=True))

    @login_required
    def get_item(self, id):
        item = self.model.query.get(id)
        if item:
            return jsonify(self.schema.dump(item))

        model_name = self.model.__name__
        return jsonify({"message": f"{model_name} not found"}), 404

    @login_required
    def create_item(self):
        data = request.get_json()
        # Remove properties that are not in the schema
        for attr in data.keys():
            if attr not in self.schema.fields:
                del data[attr]
        new_model = self.model(**data)
        db.session.add(new_model)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 400



        return jsonify(self.schema.dump(new_model))

    @login_required
    def update_item(self, id):
        item = self.model.query.get(id)
        if item:
            data = request.get_json()
            for attr, value in data.items():
                setattr(item, attr, value)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": str(e)}), 400

            return jsonify(self.schema.dump(item))

        model_name = self.model.__name__
        return jsonify({"message": f"{model_name} not found"}), 404

    @login_required
    def delete_item(self, id):
        item = self.model.query.get(id)
        if item:
            db.session.delete(item)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": str(e)}), 400
            return jsonify(self.schema.dump(item))

        model_name = self.model.__name__
        return jsonify({"message": f"{model_name} not found"}), 404

