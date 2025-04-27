from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid
from commands.extensions import db

class List(db.Model):
    __tablename__ = "list"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(50), nullable=False)
    app_uuid = Column(UUID(as_uuid=True), nullable=False)
    blocked_reason = Column(String(50), nullable=False)
    request_ip = Column(String(45), nullable=False)  # IPv6 compatible
    request_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, email, app_uuid, blocked_reason, request_ip):
        self.email = email
        self.app_uuid = app_uuid
        self.blocked_reason = blocked_reason
        self.request_ip = request_ip
        self.request_time = datetime.utcnow()
