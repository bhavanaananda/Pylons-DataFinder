import xml.etree.ElementTree as ET
from urllib import urlretrieve, urlcleanup
from datetime import datetime
import uuid
import os
import unittest
import sys
import logging
import shutil
#from logging import handlers
import logging.config
#from LogConfigParser import Config

class TestOaiClient(unittest.TestCase):
        

    def tearDown(self):
        return
    
    def setUp(self, datefile=None):
        self.until = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        print "Sdsdsdsds"
        self.metadata_formats = ['oai_dc', 'mets']
        self.verbs = ['Identify', 'ListIdentifiers', 'ListRecords', 'ListSets', 'ListMetadataFormats', 'GetRecord']
        self.args = {'from':None, 'until':self.until}
        self.oai_ns = "{http://www.openarchives.org/OAI/2.0/}"
        #self.silo = "sandbox"
  #  eprints_sources = {
  #  'maths':{'base':"http://eprints.maths.ox.ac.uk/cgi/oai2", 'records_base':'http://eprints.maths.ox.ac.uk/'}
  # ,'sbs' : {'args':"set=6F72613D54525545", 'base':"http://eureka.sbs.ox.ac.uk/cgi/oai2", 'records_base':'http://eureka.sbs.ox.ac.uk/'}
  # ,'economics':{'base':"http://economics.ouls.ox.ac.uk/cgi/oai2", 'records_base':'http://economics.ouls.ox.ac.uk/'}
  # }
        self.source = {'base':"http://eprints.maths.ox.ac.uk/cgi/oai2", 'records_base':'http://eprints.maths.ox.ac.uk/'}
        self.identifiers = []
        self.delete_identifiers = []

        self.LastModifiedFile = None
        if datefile:
              self.LastModifiedFile = datefile
        
        self.datadir = None    
        self.ids_data_file = None
        self.dc_data_file = None
        self.mods_data_file = None

        self.types = {
            'Conference or Workshop Item':'conference_item'
            ,'Monograph':'monograph'
            ,'Book':'book'
            ,'Book Section':'book_section'
            ,'Thesis':'thesis'
            ,'Article':'article'
            ,'Other':'general_item'
            ,'Artefact':'general_item'
            ,'Show/Exhibition':'general_item'
            ,'Patent':'general_item'
            ,'Teaching Resource':'general_item'
            ,'Experiment':'general_item'
            ,'Audio':'general_item'
            ,'Dataset':'general_item'
            ,'Video':'general_item'
            ,'Composition':'general_item'
            ,'Performance':'general_item'
            ,'Image':'general_item'
            ,'Technical Report':'report'
        }
		
        #c = Config()
        #logbase = c.get("app:main", "bulkuploadlog.dir")
        #logfile = os.path.join(logbase, 'bulk_uploads_logging.conf')
        #logging.config.fileConfig(logfile)
        self.logger = logging.getLogger('root')
        #oai_listIdentifiers(src=self.source)

    def set_datadir(self, pid):
        if not os.path.isdir('/tmp/eprintsdata'):
           os.mkdir('/tmp/eprintsdata')   
        self.datadir = '/tmp/eprintsdata/%s'%pid
        if os.path.isdir(self.datadir):
           shutil.rmtree(self.datadir)
        os.mkdir(self.datadir)        
        self.dc_data_file = '%s/dc_data_file.rdf'%self.datadir
        self.mods_data_file = '%s/mods_data_file'%self.datadir

    def set_from(self):
        if not os.path.isfile(self.LastModifiedFile):
            return False
        f = open(self.LastModifiedFile, 'r')
        startdate = f.read()
        startdate = startdate.strip().strip('\n')
        f.close()
        self.args['from'] = startdate
        return True

    def update_until(self):
        f = open(self.LastModifiedFile, 'w')
        f.write(self.until)
        f.close()
        return

    
    def oai_listIdentifiers(self, src={'base':"http://eprints.maths.ox.ac.uk/cgi/oai2", 'records_base':'http://eprints.maths.ox.ac.uk/'}, resumptionToken=None):
        self.ids_data_file = '/tmp/ids_data_file' ##'/tmp/%s_ids_data_file'%unicode(uuid.uuid4())
        src_url = None
        if resumptionToken:
            src_url = "%s?verb=ListIdentifiers&resumptionToken=%s"%(src['base'], resumptionToken)
        else:
            src_url = "%s?verb=ListIdentifiers&metadataPrefix=oai_dc"%src['base']
            for arg, val in self.args.iteritems():
                if val:
                    src_url = "%s&%s=%s"%(src_url, arg, val)
            if 'args' in src:
                src_url = "%s&%s"%(src_url,src['args'])
        tries = 1
        while tries < 11:
            urlretrieve(src_url, self.ids_data_file)
            if os.path.isfile(self.ids_data_file):
                self.logger.info("Downloaded identifiers for %s - %s"%(src['base'], src_url))
                break
            self.logger.warn("Error retreiving identifiers for %s - %s (try # %d)"%(src['base'], src_url, tries))
            tries += 1
        urlcleanup()
        tree = ET.ElementTree(file=self.ids_data_file)
        rt = tree.getroot()
        ids = rt.findall("%(ns)sListIdentifiers/%(ns)sheader/%(ns)sidentifier"%{'ns':self.oai_ns})
        for ID in ids:
            if resumptionToken and 'deletion' in resumptionToken:
                self.delete_identifiers.append(ID.text)
            else:
                self.identifiers.append(ID.text)
                self.oai_getDCRecord( src, ID.text, ID.text)
        rtoken = rt.findall("%(ns)sListIdentifiers/%(ns)sresumptionToken"%{'ns':self.oai_ns})
        #os.remove(self.ids_data_file)
        if rtoken:
            self.oai_listIdentifiers(src, resumptionToken=rtoken[0].text)

    def oai_getTitle(self, src, identifier):
        #Get the OAI record from the source
        src_url = "%s?verb=GetRecord&metadataPrefix=oai_dc&identifier=%s"%(src, identifier)
        tries = 1
        while tries < 11:
            urlretrieve(src_url, self.dc_data_file)
            if os.path.isfile(self.dc_data_file):
                self.logger.info("Downloaded DC for %s"%(identifier))
                break
            self.logger.error("Error retreiving DC for %s (try # %d)"%(identifier, tries))
            tries += 1
        urlcleanup()
        #Parse the document using element tree, so we can extract just the tags under oai_dc
        tree = ET.ElementTree(file=self.dc_data_file)
        rt = tree.getroot()

        #Define namespaces and add them to element tree, so it uses them.
        namespaces = {
            'oai_dc':"http://www.openarchives.org/OAI/2.0/oai_dc/"
            ,'dc':"http://purl.org/dc/elements/1.1/"
            ,'xsi':"http://www.w3.org/2001/XMLSchema-instance"
        }

        for k,v in namespaces.iteritems():
            ET._namespace_map[v] = str(k)

        #Get the DC metadata from the data
        oai_dc = rt.find("%(ns)sGetRecord/%(ns)srecord/%(ns)smetadata/{%(oai_dc)s}dc"%{'ns':self.oai_ns,'oai_dc':namespaces['oai_dc']})

        #The titles are listed as dc:title in the metadata. Get them
        record_titles = oai_dc.findall("{http://purl.org/dc/elements/1.1/}title")
        titles = []
        for t in record_titles:
            if t.text:
                titles.append(t.text)
        return titles
    
        
        
    def oai_getDCRecord(self, src, identifier, pid):
        #Get the OAI record from the source
        src_url = "%s?verb=GetRecord&metadataPrefix=oai_dc&identifier=%s"%(src['base'], identifier)
        self.set_datadir(pid)
        tries = 1
        while tries < 11:
            if os.path.isfile(self.dc_data_file):
                self.logger.info("Downloaded DC for %s - %s"%(identifier, pid))
                break
            urlretrieve(src_url, self.dc_data_file)
            self.logger.error("Error retreiving DC for %s - %s (try # %d)"%(identifier, pid, tries))
            tries += 1
        urlcleanup()
        #Parse the document using element tree, so we can extract just the tags under oai_dc
        tree = ET.ElementTree(file=self.dc_data_file)
        rt = tree.getroot()

        #Define namespaces and add them to element tree, so it uses them.
        namespaces = {
            'oai_dc':"http://www.openarchives.org/OAI/2.0/oai_dc/"
            ,'dc':"http://purl.org/dc/elements/1.1/"
            ,'xsi':"http://www.w3.org/2001/XMLSchema-instance"
        }

        for k,v in namespaces.iteritems():
            ET._namespace_map[v] = str(k)

        #Get the ID from the data header
        #Don't need to find this as ID is passed as parameter to function
        #record_id = rt.find("%(ns)sGetRecord/%(ns)srecord/%(ns)sheader/%(ns)sidentifier"%{'ns':self.oai_ns})
        #if record_id:
        #    ID = record_id.text

        #Get the DC metadata from the data
        #record_metadata = rt.find("%(ns)sGetRecord/%(ns)srecord/%(ns)smetadata"%{'ns':self.oai_ns})
        oai_dc = rt.find("%(ns)sGetRecord/%(ns)srecord/%(ns)smetadata/{%(oai_dc)s}dc"%{'ns':self.oai_ns,'oai_dc':namespaces['oai_dc']})

        #The files are listed as identifiers in the metadata. Get them and remove the id tags
        record_ids = oai_dc.findall("{http://purl.org/dc/elements/1.1/}identifier")
        files = []
        for rid in record_ids:
            if rid.text and rid.text and rid.text.startswith('http://eureka'):
                files.append(rid.text)
            oai_dc.remove(rid)

        #The types are listed as dc:type in the metadata. Get them
        record_types = oai_dc.findall("{http://purl.org/dc/elements/1.1/}type")
        types = []
        for typ in record_types:
            if typ.text and typ.text.strip() in self.types:
                types.append(self.types[typ.text.strip()])

        #The titles are listed as dc:title in the metadata. Get them
        record_titles = oai_dc.findall("{http://purl.org/dc/elements/1.1/}title")
        titles = []
        for t in record_titles:
            if t.text:
                titles.append(t.text)

        #Add the pid
        sid = ET.SubElement(oai_dc, "{http://purl.org/dc/elements/1.1/}identifier")
        sid.text = pid

        #Add the source identifier in relation
        sid = identifier.split(':')[-1]
        relele = ET.SubElement(oai_dc, "{http://purl.org/dc/elements/1.1/}relation")
        relele.text = "%s%s"%(src['records_base'], sid)

        #Add the source
        sid = identifier.split(':')[-1]
        srcele = ET.SubElement(oai_dc, "{http://purl.org/dc/elements/1.1/}source")
        srcele.text = src['records_base']

        #Write oai_dc to the file oai_dc.xml. 
        #metadata_tree = ET.ElementTree(element=oai_dc)
        #metadata_tree.write('oai_dc.xml')

        #Write the dc element to string
        dc = None
        dc = ET.tostring(oai_dc)
        if not dc:
            self.logger.warn('NO DC record for %s - %s'%(identifier, pid))
        else:
            self.logger.info('Retreived DC record for %s - %s'%(identifier, pid))

        #Return dc and list of files
        return {'dc':dc, 'files':files, 'types':types, 'titles':titles}


    def oai_getMetsModsRecord(self, src, identifier, pid):
        #example record with file "oai:eureka.sbs.ox.ac.uk:325"
        src_url = "%s?verb=GetRecord&metadataPrefix=mets&identifier=%s"%(src['base'], identifier)
        tries = 1
        while tries < 11:
            urlretrieve(src_url, self.mods_data_file)
            if os.path.isfile(self.mods_data_file):
                self.logger.info("Downloaded MODS for %s - %s"%(identifier, pid))
                break
            self.logger.error("Error retreiving MODS for %s - %s (try # %d)"%(identifier, pid, tries))
            tries += 1
        urlcleanup()
    
        #Parse the document using element tree, so we can extract just the tags under mets
        tree = ET.ElementTree(file=self.mods_data_file)
        rt = tree.getroot()

        #Define namespaces and add them to element tree, so it uses them.
        namespaces = {
            'oai_dc':"http://www.openarchives.org/OAI/2.0/oai_dc/"
            ,'mets':"http://www.loc.gov/METS/"
            ,'mods':"http://www.loc.gov/mods/v3"
            ,'xlink':"http://www.w3.org/1999/xlink"
            ,'xsi':"http://www.loc.gov/standards/mets/mets.xsd http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-0.xsd"
        }
        for k,v in namespaces.iteritems():
            ET._namespace_map[v] = str(k)
        
        #Get the MODS metadata from the data
        mets_mods = rt.find("%(ns)sGetRecord/%(ns)srecord/%(ns)smetadata/{%(mets)s}mets/{%(mets)s}dmdSec/{%(mets)s}mdWrap/{%(mets)s}xmlData"%{'ns':self.oai_ns,'mets':namespaces['mets']})

        #Add the pid
        spid = ET.SubElement(mets_mods, "{http://www.loc.gov/mods/v3}identifier",  attrib={"type":"pid"})
        spid.text = pid
        surn = ET.SubElement(mets_mods, "{http://www.loc.gov/mods/v3}identifier",  attrib={"type":"urn"})
        surn.text = pid

        #Add the source id as another version
        sid = identifier.split(':')[-1]
        sida = ET.SubElement(mets_mods, "{http://www.loc.gov/mods/v3}relatedItem",  attrib={"type":"otherVersion"})
        sidb = ET.SubElement(sida, "{http://www.loc.gov/mods/v3}location")
        sidc = ET.SubElement(sidb, "{http://www.loc.gov/mods/v3}url")
        sidc.text = "%s%s"%(src['records_base'], sid)

        #Add the source as record content source
        srcele = ET.SubElement(mets_mods, "{http://www.loc.gov/mods/v3}recordInfo")
        srceleb = ET.SubElement(srcele, "{http://www.loc.gov/mods/v3}recordContentSource")
        srceleb.text = src['records_base']

        #Write the mods element to string and replace mets tag with mods tag
        MODS = None
        MODS = ET.tostring(mets_mods)
        if not MODS:
            self.logger.warn('NO MODS record for %s - %s'%(identifier, pid))
        else:
            self.logger.info('Retreived MODS record for %s - %s'%(identifier, pid))
        MODS = MODS.replace("""<mets:xmlData xmlns:mets="http://www.loc.gov/METS/">""", """<mods:modsCollection xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://ora.ox.ac.uk/access/mods-3.2-oxford.xsd">
  <mods:mods version="3.2">""")
        MODS = MODS.replace("""</mets:xmlData>""", """
  </mods:mods>
</mods:modsCollection>""")

        #Get the list of files
        files = []
        mets_files = rt.findall("%(ns)sGetRecord/%(ns)srecord/%(ns)smetadata/{%(mets)s}mets/{%(mets)s}fileSec/{%(mets)s}fileGrp/{%(mets)s}file"%{'ns':self.oai_ns,'mets':namespaces['mets']})
        for m in mets_files:
            size = m.get('SIZE')
            mt = m.get('MIMETYPE')
            flocat = m.find("{%(mets)s}FLocat"%{'mets':namespaces['mets']})
            loc = flocat.get('{%(xlink)s}href'%{'xlink':namespaces['xlink']})
            files.append((loc, mt, size))
        return {'mods':MODS, 'files':files}
    
    def retreiveFiles(self, files):
        files_retreived = []
        for f in files:
            fn = f[0].strip('/').split('/')[-1]
            floc = '%s/%s'%(self.datadir, fn)
            tries = 1
            while True:
                urlretrieve(f[0], floc)
                if os.path.isfile(floc):
                    if str(os.path.getsize(floc)) == f[2]:
                        urlcleanup()
                        self.logger.info('Retreived file %s'%f[0])
                        break
                    else:
                        self.logger.warn('Download file size does not match metadata %s (try # %d)'%(f[0], tries))
                else:
                    self.logger.warn('Error retreiving file %s (try # %d)'%(f[0], tries))
                tries += 1
                if tries > 10:
                    break
            files_retreived.append((f[0], f[1], f[2], floc))
        return files_retreived


    def testUnits(self):
        assert (True)

    def testComponents(self):
        assert (True)

    def testIntegration(self):
        assert (True)

    def testPending(self):
        assert (False), "No pending test"

# Assemble test suite

import TestUtils

def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"      return suite of unit tests only
            "component" return suite of unit and component tests
            "all"       return suite of unit, component and integration tests
            "pending"   return suite of pending tests
            name        a single named test to be run
    """
    testdict = {
        "unit": 
            [ 
             "oai_listIdentifiers"
            ],
        "component":
            [ "testComponents"
            ],
        "integration":
            [ "testIntegration"
            ],
        "pending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestOaiClient, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestOaiClient.log", getTestSuite, sys.argv)

# End.



   
