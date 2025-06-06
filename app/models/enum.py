import enum
from sqlalchemy.dialects.postgresql import ENUM as SQLEnum

class GenderEnum(enum.Enum):
    MALE = 'male'
    FEMALE = 'female' 
    OTHER = 'others'