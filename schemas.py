import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, LargeBinary, JSON, func, DateTime, ARRAY, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from constants import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import databases
import secrets



Base = declarative_base()
engine = create_engine(DATABASE_URL)


class SMTPSettings(Base):
    __tablename__ = "smtp_settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    smtp_server = Column(String, nullable=True)
    smtp_port = Column(Integer, nullable=True)
    smtp_username = Column(String, nullable=True)
    smtp_password = Column(String, nullable=True)
    sender_email = Column(String, nullable=True)

    user = relationship("User", back_populates="smtp_settings")


class EmailTemplate(Base):
    __tablename__ = 'email_templates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    subject = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)

    def __repr__(self):
        return f'<EmailTemplate(name={self.name}, user_id={self.user_id})>'


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    token = Column(String, default="")
    stripe_customer_id = Column(String, unique=True)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    profile_picture = Column(String, nullable=True)
    status = Column(String, default="active", index=True)

    resume_data = relationship("ResumeData", back_populates="user")
    password_resets = relationship("PasswordReset", back_populates="user")
    services = relationship("Service", secondary="user_services")
    company = relationship("Company", back_populates="user")
    smtp_settings = relationship("SMTPSettings", uselist=False, back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    posts = relationship("Post", back_populates="user")
    categories = relationship("Category", back_populates="user")
    subcategories = relationship("SubCategory", back_populates="user")
    tags = relationship("Tag", back_populates="user")

    media = relationship("Media", back_populates="user")

    newsletter_subscriptions = relationship('NewsLetterSubscription', back_populates='user')


class Service(Base):

    __tablename__ = 'services'

    service_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)

    users = relationship("User", secondary="user_services")

class UserServices(Base):
    __tablename__ = 'user_services'

    user_service_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    service_id = Column(Integer, ForeignKey('services.service_id'))


class ResumeData(Base):
    __tablename__ = "resume_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    extracted_data = Column(JSON)
    csv_file = Column(LargeBinary)
    xml_file = Column(LargeBinary)
    upload_datetime = Column(DateTime(timezone=True), server_default=func.now())
    # pdf_resumes = Column(ARRAY(LargeBinary))

    user = relationship("User", back_populates="resume_data")

class Plan(Base):
    __tablename__ = 'plans'

    id = Column(Integer, primary_key=True)
    plan_type_name = Column(String)
    time_period = Column(String)   #months
    fees = Column(Integer)
    num_resume_parse = Column(String)
    plan_details = Column(String)
    stripe_product_id = Column(String) # New field for Stripe Product ID
    stripe_price_id = Column(String)

    subscriptions = relationship("Subscription", back_populates="plan")

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    stripe_subscription_id = Column(String, unique=True)
    stripe_customer_id = Column(String)
    plan_id = Column(Integer, ForeignKey('plans.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String) # e.g., 'active', 'past_due', 'canceled', etc.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")
    plan = relationship('Plan', back_populates='subscriptions')


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, default=secrets.token_urlsafe)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="password_resets")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="company")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    author_name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))  # Updated to store category ID
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'))  # Updated to store subcategory ID
    tag_id = Column(Integer, ForeignKey('tags.id'))
    status = Column(String, default="published", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    subcategory = relationship("SubCategory", back_populates="posts")
    tag = relationship("Tag", back_populates="posts")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="categories")
    posts = relationship("Post", back_populates="category")

class SubCategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)
    subcategory = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="subcategories")
    posts = relationship("Post", back_populates="subcategory")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="tags")
    posts = relationship("Post", back_populates="tag")



class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="media")

######################################################### NEWSLETTER ######################################################################


class NewsLetterSubscription(Base):
    __tablename__ = 'newsletter_subscriptions'
    id = Column(Integer, primary_key=True)
    subscriber_name = Column(String)
    subscriber_email = Column(String)
    status = Column(String, default="active", index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User', back_populates='newsletter_subscriptions')





# Create all tables defined in the metadata
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")


# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

