from enum import unique
from app import db
from datetime import datetime
# from hashlib import md5
# from werkzeug.security import generate_password_hash, check_password_hash

class VideoMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    youtube_id = db.Column(db.String(256), unique=True)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speaker.id'))
    is_published = db.Column(db.Boolean)

    def __repr__(self) -> str:
        # v = VideoMessage(title='Evangelist Danny Long', description='For the Son of man is come to seek and to save that which was lost.', youtube_id='X_tZxywMJWM', timestamp=datetime(2021, 7, 4, 14, 45, 0))
        # db.session.add(v)
        # db.session.commit()
        # VideoMessage(title='Them That Dwell On the Earth', description='Revelation 14:6-11', youtube_id='_xTc7RHmISE', timestamp=datetime(2021, 6, 27, 14, 45, 0))
        # VideoMessage(title='Jairus Besought Him Greatly', description='Mark 5:21-24, 35-43', youtube_id='w4c74k2BKUc', timestamp=datetime(2021, 6, 20, 14, 45, 0))
        # VideoMessage(title='Another beast coming up out of the earth', description='Revelation 13:11-15', youtube_id='o8ZM5zxqNGc', timestamp=datetime(2021, 6, 6, 14, 45, 0))
        # VideoMessage(title='The Mark of the Beast', description='Revelation 13:16-18', youtube_id='3BBf0TmIMAY', timestamp=datetime(2021, 6, 13, 14, 45, 0))
        # VideoMessage(title='Remember the Lord thy God', description='Deuteronomy 8:10-17', youtube_id='05M_RkGE2Ts', timestamp=datetime(2021, 5, 30, 14, 45, 0))
        # insert into video_message(title,description,timestamp,youtube_id) values('The Time Is Come','Revelation 14:14-20','2021-07-11 14:45:00.000','kN6m--IF3Xc');
        return f'VideoMessage:"{self.title} - {self.description}" Id:{self.id}, Timestamp:{self.timestamp}, YouTubeId:{self.youtube_id} IsPublished:{self.is_published} SpeakerId:{self.speaker_id}'

class Speaker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    icon_file_name = db.Column(db.String(128))
    is_guest = db.Column(db.Boolean)
    description = db.Column(db.String(512))
    messages = db.relationship('VideoMessage', backref='speaker', lazy='dynamic')

    def __repr__(self) -> str:
        return f'Speaker: "{self.first_name} {self.last_name}" Id:{self.id} IsGuest:{self.is_guest} IconFileName:{self.icon_file_name}'