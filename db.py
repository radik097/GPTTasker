from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'mysql+pymysql://task_user:secure_password@localhost/task_manager'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
