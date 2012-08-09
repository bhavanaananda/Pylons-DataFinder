"""Setup the datafinder application"""
import logging

from datafinder.config.environment import load_environment
from datafinder.model import meta, SourceInfo
from sqlalchemy.exc import IntegrityError

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup datafinder here"""
    # Don't reload the app if it was loaded under the testing environment
    load_environment(conf.global_conf, conf.local_conf)
    log.info("Creating tables")
    print "Creating tables"
    meta.metadata.create_all(bind=meta.engine)
    log.info("Successfully setup")
    print "Successfully setup"
 
    try:
        sourceinfo = SourceInfo()
        sourceinfo.silo= u'webtesttest'
        meta.Session.add(sourceinfo)
        meta.Session.flush()
        meta.Session.commit()
    except IntegrityError:
        log.error('there was a problem adding your auth data, it may have already been added. Continuing with bootstrapping...')
        print 'there was a problem adding your auth data, it may have already been added. Continuing with bootstrapping...'
        #import traceback
        #print traceback.format_exc()
        meta.Session.rollback()
