# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AppLicenseRecord(Base):
    __tablename__ = 'app_license_record'

    id = Column(INTEGER(11), primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP)
    app_info = Column(String(3000))
    logic_switch = Column(String(8192), nullable=False, server_default=text("''"))
    app_corp_name = Column(String(100), nullable=False, server_default=text("''"))
    start = Column(BIGINT(20))
    end = Column(BIGINT(20))
    pkg_expr = Column(String(256))
    name = Column(String(64))
    os_platform = Column(TINYINT(4))
    func_config = Column(String(4096), nullable=False, server_default=text("''"))
    dlive_info = Column(INTEGER(11))
    business_url = Column(String(2000))
    download_url = Column(String(2000))
    license_key = Column(String(2000))
