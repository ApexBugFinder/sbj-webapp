from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os, sys
import tempfile
import pytest
from decouple import config
sys.path.append("../../../../sbj")
import app
@pytest.fixture
def tester():
      tester = app.create_app(test_config=True)
      return tester




