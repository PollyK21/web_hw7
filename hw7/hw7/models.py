from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_code = Column(Integer, unique=True, nullable=False)


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey(Groups.id))


class Teachers(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)


class Subjects(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey(Teachers.id))


class Marks(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey(Students.id, ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey(Subjects.id, ondelete="CASCADE"))
    grade = Column(Integer)
    date = Column(Date, nullable=False)
