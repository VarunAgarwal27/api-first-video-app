from datetime import datetime

class VideoModel:
    def __init__(self, db):
        self.collection = db.videos

    def create_video(self, title, description, youtube_id, thumbnail_url):
        video = {
            "title": title,
            "description": description,
            "youtube_id": youtube_id,
            "thumbnail_url": thumbnail_url,
            "is_active": True,
            "created_at": datetime.utcnow()
        }

        self.collection.insert_one(video)
        return video

    def get_active_videos(self, limit=2):
        return list(
            self.collection.find({"is_active": True}).limit(limit)
        )

    def get_by_id(self, video_id):
        from bson.objectid import ObjectId
        return self.collection.find_one({"_id": ObjectId(video_id)})
