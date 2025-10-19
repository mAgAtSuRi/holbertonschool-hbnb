from flask_restx import Namespace, Resource, fields
from ...services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        # Placeholder for the logic to register a new review
        review_data = api.payload

        required_field = ["comment", "rating", "user_id", "place_id"]
        for field in required_field:
            if field not in review_data:
                return {"error": f"Missing required field: {field}"}, 400
        
        user = facade.get_user(review_data["user_id"])
        if not user:
            return {"error": f"User id not found: {review_data["user_id"]}"}, 404
        
        place = facade.get_place(review_data["place_id"])
        if not place:
            return {"error": f"Place id not found: {review_data['place_id']}"}, 404

        new_review = facade.create_review(review_data)
        return new_review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        reviews = facade.review_repo.get_all()
        return [review.to_dict() for review in reviews]

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        review = facade.get_review(review_id)
        if not review:
            return {"error": f"Review not found"}, 404
        return review.to_dict()

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        deleted_review = facade.delete_review(review_id)
        if not deleted_review:
            return {"error": "Review not found"}, 400
        return {"message": "review deleted successfully"}, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Placeholder for the logic to update a review by ID
        review = facade.get_review(review_id)
        if not review:
            return {"error": "review not found"}, 404

        review_data = api.payload
        review_data.pop("place_id", None)
        review_data.pop("user_id", None)
       
        required_field = ["rating", "comment"]
        for field in required_field:
            if field not in review_data:
                return {"error": f"Missing required field: {field}"}, 400

        facade.update_review(review_id, review_data)
        updated_review = facade.get_review(review_id)
        return updated_review.to_dict()

