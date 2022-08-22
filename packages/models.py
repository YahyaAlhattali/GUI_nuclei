from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Text,DateTime
from sqlalchemy.orm import relationship
from packages.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    ver_code = Column(String)

class Scan(Base):
    __tablename__="scan"
    id= Column(Integer, primary_key=True,index=True,autoincrement=True)
    domain = Column(String, index=True)
    time_started= Column(DateTime, default=datetime.utcnow())
    time_finshed=Column(DateTime,index=True)
    progress_status =Column(String,index=True)
    description= Column(Text,index=True)
    template_used= Column(String,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    logs= relationship("Logs",cascade="all, delete")
    vulns = relationship("Vulnerabilities",cascade="all, delete")
class Vulnerabilities(Base):
    __tablename__="vulnerabilities"
    id= Column(Integer, primary_key=True,index=True)
    Type= Column(String, index=True)
    Title= Column(String, index=True)
    Severity= Column(String, index=True)
    CVSS_Score= Column(String, index=True)
    CVE_CWE= Column(String, index=True)
    Vulnerable_URL= Column(String, index=True)
    Description= Column(String, index=True)
    Discovered_on= Column(String, index=True)
    scan_id=Column(Integer, ForeignKey("scan.id",ondelete="CASCADE"))

class Logs(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    des =Column(Text,index=True)
    scan = Column(Integer,ForeignKey("scan.id",ondelete="CASCADE"))