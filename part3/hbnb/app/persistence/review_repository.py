from app.models.review import Review
from ..extensions import db


class ReviewRepository:
    def create(self, data):
        review = Review(**data)
        db.session.add(review)
        db.session.commit()
        return review

    def get_all(self):
        return Review.query.all()

    def get_by_id(self, review_id):
        return Review.query.get(review_id)

    def update(self, review_id, data):
        review = self.get_by_id(review_id)
        if not review:
            raise LookupError(f"Review not found: {review_id}")

        for key, value in data.items():
            if hasattr(review, key):
                setattr(review, key, value)

        db.session.commit()
        return review

    def delete(self, review_id):
        review = self.get_by_id(review_id)
        if not review:
            raise LookupError(f"Review not found: {review_id}")

        db.session.delete(review)
        db.session.commit()
        return True
