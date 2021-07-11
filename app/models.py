from enum import unique
from app import db
from datetime import datetime
# from hashlib import md5
# from werkzeug.security import generate_password_hash, check_password_hash

class VideoMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    youtube_id = db.Column(db.String(256), unique=True)

    def __repr__(self):
        # v = VideoMessage(title='Evangelist Danny Long', description='For the Son of man is come to seek and to save that which was lost.', youtube_id='X_tZxywMJWM', timestamp=datetime(2021, 7, 4, 14, 45, 0))
        # db.session.add(v)
        # db.session.commit()
        # VideoMessage(title='Them That Dwell On the Earth', description='Revelation 14:6-11', youtube_id='_xTc7RHmISE', timestamp=datetime(2021, 6, 27, 14, 45, 0))
        # VideoMessage(title='Jairus Besought Him Greatly', description='Mark 5:21-24, 35-43', youtube_id='w4c74k2BKUc', timestamp=datetime(2021, 6, 20, 14, 45, 0))
        # VideoMessage(title='Another beast coming up out of the earth', description='Revelation 13:11-15', youtube_id='o8ZM5zxqNGc', timestamp=datetime(2021, 6, 6, 14, 45, 0))
        # VideoMessage(title='The Mark of the Beast', description='Revelation 13:16-18', youtube_id='3BBf0TmIMAY', timestamp=datetime(2021, 6, 13, 14, 45, 0))
        # VideoMessage(title='Remember the Lord thy God', description='Deuteronomy 8:10-17', youtube_id='05M_RkGE2Ts', timestamp=datetime(2021, 5, 30, 14, 45, 0))
        return f'VideoMessage:"{self.title}" Id:{self.id}, Timestamp:{self.timestamp}, YouTubeId:{self.youtube_id}'