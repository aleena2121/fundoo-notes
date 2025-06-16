# Import all model modules to ensure mappers are configured
from app.models import user_model, labels_model, notes_model, association
from sqlalchemy.orm import configure_mappers

# Force mapper configuration
configure_mappers()
