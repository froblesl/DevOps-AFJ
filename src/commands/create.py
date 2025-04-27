import logging
from .extensions import db
from models.model import List
import uuid

logger = logging.getLogger(__name__)

class Create:
    def __init__(self, email, app_uuid, blocked_reason, request_ip):
        self.email = email
        self.app_uuid = uuid.UUID(app_uuid) if isinstance(app_uuid, str) else app_uuid
        self.blocked_reason = blocked_reason
        self.request_ip = request_ip

    def execute(self):
        try:
            nuevo_item = List(
                email=self.email,
                app_uuid=self.app_uuid,
                blocked_reason=self.blocked_reason,
                request_ip=self.request_ip
            )
            db.session.add(nuevo_item)
            db.session.commit()

            logger.info("Se ha creado una entrada en la tabla 'list' con ID: %s", nuevo_item.id)

            return {
                "id": str(nuevo_item.id),
                "email": nuevo_item.email,
                "request_ip": nuevo_item.request_ip
            }

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error inesperado al crear la entrada: {str(e)}")
            raise
