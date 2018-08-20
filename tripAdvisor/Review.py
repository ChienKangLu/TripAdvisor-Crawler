import json

class Review:
    def __init__(self, poi_id,uid,review_title,review_rating,review,ratingDate):
        self.poi_id=str(poi_id)
        self.uid=uid
        self.review_title=review_title
        self.review_rating=review_rating
        self.review=review
        self.ratingDate=ratingDate

    def toJson(self):
        # return json.dumps(self.__dict__,indent=4,ensure_ascii=False)
        return json.dumps(self.__dict__, ensure_ascii=False)

    def __str__(self):
        return self.toJson()





