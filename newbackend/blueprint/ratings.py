from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import current_user, login_required
from application import db
from application.models import Ratings, Product, User

rating_bp = Blueprint('rating', __name__)

from flask import jsonify

@rating_bp.route('/rate_product/<int:productID>', methods=['GET', 'POST'])
@jwt_required()
def rate_product(productID):
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()
    product = Product.query.filter_by(id=productID).first()
    if request.method == 'GET':
        try:
            # Fetch the current rating for the product
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            current_rating = product.rating if product.rating else 0

            return jsonify({'current_rating': current_rating}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            print(user.id)
            print(productID)
            stars = data.get('stars')
            print(stars)
            # Create a new rating
            new_rating = Ratings(product_id=productID, revie_number=stars, review=None, user_id=user.id)
            db.session.add(new_rating)
            db.session.commit()
            # Update the average rating for the product
            product_ratings = [rating.revie_number for rating in product.ratings]
            product.rating = sum(product_ratings) / len(product_ratings)
            db.session.commit()
            # Fetch the current rating for the product after the update
            current_rating = product.rating if product.rating else 0

            return jsonify({'success': 'Rating submitted successfully', 'current_rating': current_rating}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
