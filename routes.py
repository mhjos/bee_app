import random
from flask import request, jsonify, session
from models import Hive, Bee, db

def init_routes(app):

    # ---- Hive CRUD ----
    @app.route('/hives', methods=['GET'])
    def get_all_hives():
        hives = Hive.query.all()
        return jsonify([
            {'id': h.id, 'name': h.name, 'honey': h.honey}
            for h in hives
        ]), 200
    
    @app.route('/hives/<int:hive_id>', methods=['GET'])
    def get_hive(hive_id):
        hive = Hive.query.get_or_404(hive_id)
        return jsonify({
            'id': hive.id,
            'name': hive.name,
            'honey': hive.honey
        }), 200

    @app.route('/hives', methods=['POST'])
    def create_hive():
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        hive = Hive(name=data['name'], honey=0)
        db.session.add(hive)
        db.session.commit()
        return jsonify({'message': 'Hive created', 'id': hive.id, 'honey': hive.honey}), 201

    @app.route('/hives/<int:hive_id>', methods=['PUT'])
    def update_hive(hive_id):
        hive = Hive.query.get_or_404(hive_id)
        data = request.get_json()
        hive.name = data.get('name', hive.name)
        db.session.commit()
        return jsonify({'message': 'Hive updated', 'id': hive.id, 'honey': hive.honey}), 200

    @app.route('/hives/<int:hive_id>', methods=['DELETE'])
    def delete_hive(hive_id):
        hive = Hive.query.get_or_404(hive_id)
        db.session.delete(hive)
        db.session.commit()
        return jsonify({'message': 'Hive deleted'}), 200

    # ---- Bee Login / Create / Logout ----
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        
        bee = Bee.query.filter_by(name=data['name']).first()
        if bee:
            # Increase pollen randomly between 2 and 10
            gained_pollen = random.randint(2, 10)
            bee.pollen += gained_pollen
            db.session.commit()

            session['bee_id'] = bee.id
            session['bee_name'] = bee.name
            
            return jsonify({
                'message': f'Logged in as {bee.name}. Gained {gained_pollen} pollen!',
                'bee': {'id': bee.id, 'name': bee.name, 'pollen': bee.pollen}
            }), 200
        
        return jsonify({'error': 'Bee not found'}), 404

    @app.route('/create_bee', methods=['POST'])
    def create_bee():
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        existing = Bee.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Bee already exists'}), 400
        bee = Bee(name=data['name'], pollen=0)
        db.session.add(bee)
        db.session.commit()
        session['bee_id'] = bee.id
        session['bee_name'] = bee.name
        return jsonify({
            'message': f'Bee {bee.name} created and logged in',
            'bee': {'id': bee.id, 'name': bee.name, 'pollen': bee.pollen}
        }), 201

    @app.route('/logout', methods=['POST'])
    def logout():
        session.clear()
        return jsonify({'message': 'Logged out'}), 200

    # ---- Optional: Gamification routes ----
    @app.route('/bees/<int:bee_id>/deduct_pollen', methods=['POST'])
    def deduct_pollen(bee_id):
        bee = Bee.query.get_or_404(bee_id)
        data = request.get_json()
        amount = data.get('amount', 0)
        
        if bee.pollen < amount:
            return jsonify({'error': 'Not enough pollen'}), 400
        
        bee.pollen -= amount
        db.session.commit()
        
        return jsonify({'message': f'{amount} pollen deducted', 'pollen': bee.pollen}), 200
     
    @app.route('/bees/<int:bee_id>/collect_pollen', methods=['POST'])
    def collect_pollen(bee_id):
        bee = Bee.query.get_or_404(bee_id)
        bee.pollen += 5
        db.session.commit()
        return jsonify({'message': f'{bee.name} collected pollen', 'pollen': bee.pollen}), 200

    @app.route('/hives/<int:hive_id>/add_honey', methods=['POST'])
    def add_honey(hive_id):
        hive = Hive.query.get_or_404(hive_id)
        data = request.get_json()
        amount = data.get('amount', 0)
        hive.honey += amount
        db.session.commit()
        return jsonify({'message': f'{amount} honey added', 'honey': hive.honey}), 200

