'''
Created on 1 maj 2018

@author: thomasg
'''


from os import path, makedirs

from pprint import pprint
from collections import OrderedDict
import json
import copy
    
class WriteJson:
    '''
    '''
    def __init__(self, XMLFPN, nodeChildD, bandD, spectraD, tuningD,  sceneD,  annotateD, sampleD):
        '''
        '''
        self.XMLFPN = XMLFPN
        self.nodeChildD = nodeChildD
        self.bandD = bandD
        self.spectraD = spectraD
        self.tuningD = tuningD
        self.sceneD = sceneD
        
        self.annotateD = annotateD
        self.sampleD = sampleD
        
        if self.nodeChildD['classification']['siteid'] == '*':
            self.nodeChildD['classification']['siteid'] = self.nodeChildD['classification']['tractid']

        
        self.WriteProbe()
        
        self.WriteInstrument()
        
        self.WriteCollection()
           
        self.WriteSample()
        
        self.WriteSampleAuxiliary()
        
        self.WriteModel()
        
        
    def ModelParams(self):
        '''
        '''
        
        featureLineD = OrderedDict()
        
        featureLineD['abundanceMax'] = self.nodeChildD['featurelineXY']['densitymax']
        featureLineD['abundanceMin'] = self.nodeChildD['featurelineXY']['densitymin']
        featureLineD['coverageRescale'] = self.nodeChildD['featurelineXY']['COVrescale']

        
        featureLineD['planes'] = OrderedDict()
        
        featureLineD['planes']['0'] = OrderedDict()
        
        featureLineD['planes']['0']['xcrossPercent'] = self.nodeChildD['featurelineXY']['featureXp']
        featureLineD['planes']['0']['ycrossPercent'] = self.nodeChildD['featurelineXY']['featureYp']        
        featureLineD['planes']['0']['convergenceFactor'] = self.nodeChildD['featurelineXY']['Cfac']
        featureLineD['planes']['0']['similarityFactor'] = self.nodeChildD['featurelineXY']['SIMfac']

        featureLineD['planes'] = OrderedDict()
        
        featureLineD['planes']['1'] = OrderedDict()
        
        featureLineD['planes']['1']['xcrossPercent'] = self.nodeChildD['featurelineYZ']['featureXp']
        featureLineD['planes']['1']['ycrossPercent'] = self.nodeChildD['featurelineYZ']['featureYp']        
        featureLineD['planes']['1']['convergenceFactor'] = self.nodeChildD['featurelineYZ']['Cfac']
        featureLineD['planes']['1']['similarityFactor'] = self.nodeChildD['featurelineYZ']['SIMfac']

        calibrationD = OrderedDict()
        
        calibrationD['abundanceMaxMin'] = self.nodeChildD['featurelineXY']['densitymax']
        calibrationD['abundanceMaxMax'] = self.nodeChildD['featurelineXY']['densitymax']
  
        calibrationD['abundanceMin'] = self.nodeChildD['featurelineXY']['densitymin']
        calibrationD['coverageRescale'] = self.nodeChildD['featurelineXY']['COVrescale']

        
        calibrationD['planes'] = OrderedDict()
        
        calibrationD['planes']['0'] = OrderedDict()
        
        calibrationD['planes']['0']['xcrossPercentMax'] = self.nodeChildD['featurelineXY']['featureXp']
        calibrationD['planes']['0']['xcrossPercentMin'] = self.nodeChildD['featurelineXY']['featureXp']        
        calibrationD['planes']['0']['ycrossPercentMax'] = self.nodeChildD['featurelineXY']['featureYp']
        calibrationD['planes']['0']['ycrossPercentMin'] = self.nodeChildD['featurelineXY']['featureYp'] 
        calibrationD['planes']['0']['convergenceFactorMax'] = self.nodeChildD['featurelineXY']['Cfac']
        calibrationD['planes']['0']['convergenceFactorMin'] = self.nodeChildD['featurelineXY']['Cfac'] 
                
        calibrationD['planes']['0']['similarityFactorMax'] = self.nodeChildD['featurelineXY']['SIMfac']
        calibrationD['planes']['0']['similarityFactorMin'] = self.nodeChildD['featurelineXY']['SIMfac']

        calibrationD['planes'] = OrderedDict()
        
        calibrationD['planes']['1'] = OrderedDict()
        
        calibrationD['planes']['1']['xcrossPercentMax'] = self.nodeChildD['featurelineYZ']['featureXp']
        calibrationD['planes']['1']['xcrossPercentMin'] = self.nodeChildD['featurelineYZ']['featureXp']        
        calibrationD['planes']['1']['ycrossPercentMax'] = self.nodeChildD['featurelineYZ']['featureYp']
        calibrationD['planes']['1']['ycrossPercentMin'] = self.nodeChildD['featurelineYZ']['featureYp'] 
        calibrationD['planes']['1']['convergenceFactorMax'] = self.nodeChildD['featurelineYZ']['Cfac']
        calibrationD['planes']['1']['convergenceFactorMin'] = self.nodeChildD['featurelineYZ']['Cfac'] 
                
        calibrationD['planes']['1']['similarityFactorMax'] = self.nodeChildD['featurelineYZ']['SIMfac']
        calibrationD['planes']['1']['similarityFactorMin'] = self.nodeChildD['featurelineYZ']['SIMfac']

        return featureLineD, calibrationD
    
    def WriteModel(self):  
        '''
        '''
        #bandsaliasL = ['BL','GL','RL','NA','MB','MC']
        
        featureLineD, calibrationD = self.ModelParams()
        
        remain,splitoff = path.split(self.XMLFPN)
        remain,date_date = path.split(remain)
        remain,sample = path.split(remain)
        remain,statstype = path.split(remain)
        
        year = date_date[0:4]
        ustats = statstype[2:len(statstype)]
        sampleL = sample.lower().split('-')
        
        specs = '%(s)s-%(u)s-slope%(t)s' %{'s':sampleL[0],'u':ustats,'t':sampleL[2]}
        title =  '%(p)s %(s)s %(u)s slope <= %(t)s degree, %(y)s' %{'p':self.nodeChildD['classification']['tractid'],'s':sampleL[0],'u':ustats,'t':sampleL[2], 'y':year}
        description = 'Landsat ETM model for forest biomass in the Czech Republic'
                       
        fp = path.join(self.nodeChildD['target']['path'],'models',
                self.nodeChildD['classification']['phylum'],
                self.nodeChildD['classification']['class'],
                self.nodeChildD['classification']['order'],
                self.nodeChildD['classification']['family'],
                self.nodeChildD['classification']['tractid'])
        
        if not path.exists(fp):
            makedirs(fp)
           
        fn =  '%(id)s-%(s)s-%(y)s.json' %{'id':self.nodeChildD['collection']['id'],'s':specs, 'y':year} 
        
        fpn = path.join(fp,fn)

        if not path.exists(fpn):
            print (fpn)

        modelD = OrderedDict ([ ('id',path.split(fn)[0]), 
                            ('title',title),
                            ('description', description),
                            ('collection',self.nodeChildD['collection']['id'])])
        
        for item in self.nodeChildD['classification']:
            modelD[item] = self.nodeChildD['classification'][item]
 
                                                   
        sampleid = self.spectraD[ self.nodeChildD['orthofeatures']['tcfeature'] ]['sampleid']
        
        modelD['targetFeature'] = sampleid
        modelD['targetFeatureSource'] = "sample"
        
        
        modelD['featureLine'] = featureLineD
        
        modelD['calibration'] = calibrationD
        
        modelD['orthoEntities'] = OrderedDict()
        
        modelD['orthoEntities'] = OrderedDict()
        modelD['orthoEntitiesSource'] = OrderedDict()
        modelD['orthoEntities']['offset'] = self.nodeChildD['orthofeatures']['tcoffset']
        
        eigenVectorsL = [self.spectraD[ self.nodeChildD['orthofeatures']['tc1'] ]['sampleid'],
                         self.spectraD[ self.nodeChildD['orthofeatures']['tc2'] ]['sampleid'],
                         sampleid]
        modelD['orthoEntities']['eigenVectors'] = eigenVectorsL
        
        modelD['orthoEntitiesSource']['offset'] = 'matrixElement'
        eigenVectorsSourceL = ['matrixElement',
                         'matrixElement',
                         'sample']
        modelD['orthoEntitiesSource']['eigenVectors'] = eigenVectorsSourceL
        
        domainD = OrderedDict()
        domainD['logTrans'] = 0
        domainD['expTrans'] = 0
        domainD['planes'] = OrderedDict()
        
        domainD['planes']["0"] = [self.spectraD[ self.nodeChildD['orthofeatures']['tc1'] ]['sampleid'] ,self.spectraD[ self.nodeChildD['orthofeatures']['tc2'] ]['sampleid']]
        domainD['planes']["1"] = [self.spectraD[ self.nodeChildD['orthofeatures']['tc2'] ]['sampleid'],sampleid]

        matrixElementsD = OrderedDict()

        if modelD['orthoEntitiesSource']['offset'] == 'matrixElement':
  
            elment = self.spectraD[ modelD['orthoEntities']['offset'] ]['sampleid']
            matrixElementsD[elment] = {}
            matrixElementsD[elment]['aggregation'] = 'xspectre_landsat_soilline_pub'
            matrixElementsD[elment]['collection'] = self.nodeChildD['collection']['id']
            matrixElementsD[elment]['touch'] = 2
                     
            #bandL = []
            #for b in bandsaliasL:
            #    bandL.append(self.spectraD[elment]['values'][b])
            #matrixElementsD[elment]['spectra'] = bandL
           
        for i,mES in enumerate(modelD['orthoEntitiesSource']['eigenVectors']):
            if mES == 'matrixElement':
                elment = modelD['orthoEntities']['eigenVectors'][i]   
                matrixElementsD[elment] = {}
                matrixElementsD[elment]['aggregation'] = 'xspectre_landsat_soilline_pub'
                matrixElementsD[elment]['collection'] = self.nodeChildD['collection']['id']
                matrixElementsD[elment]['touch'] = 2
                bandL = []
                #for b in bandsaliasL:
                #    bandL.append(self.spectraD[elment]['values'][b])
                #matrixElementsD[elment]['spectra'] = bandL

        samplesD = {}
        
        for s in self.spectraD:
  
            if self.spectraD[s]['category'][0:3].lower() in ['cal','val','ref']:
                sampleid = self.spectraD[s]['sampleid']
                #sid = '%(plotid)s_%(specimen)s' %{'plotid':s,'specimen':self.spectraD[s]['species']}
                samplesD[sampleid] = {}
                #samplesD[sid]['aggregation'] = self.nodeChildD['aggregation']['id']
                samplesD[sampleid]['collection'] = self.nodeChildD['collection']['id']
                samplesD[sampleid]['category'] = 'calibration'
                #samplesD[sid]['specimen'] = self.spectraD[s]['species']
                
                #samplesD[s]['abundance'] = self.spectraD[s]['density']
                #samplesD[sampleid]['touch'] = self.spectraD[s]['use']
                #bandL = []
                #for b in bandsaliasL:
                #    bandL.append(self.spectraD[s]['values'][b])
                #samplesD[s]['spectra'] = bandL
            
        # put together model, matrixelemens and spectra
        
        modelD["domain"] = domainD
        modelD["matrixElements"] = matrixElementsD
        modelD["samples"] = samplesD
        
        with open(fpn, 'w') as outfile:
            json.dump(modelD, outfile)
   
    def WriteCollection(self): 
        '''
        '''
        
        # Write the collection for the samples
        fp = path.join(self.nodeChildD['target']['path'],'collections',
                self.nodeChildD['classification']['phylum'],
                self.nodeChildD['classification']['class'],
                self.nodeChildD['classification']['order'],
                self.nodeChildD['classification']['family'],
                self.nodeChildD['classification']['tractid'])
        
        if not path.exists(fp):
            makedirs(fp)
           
        fn =  '%(cid)s.json' %{'cid':self.nodeChildD['collection']['id']} 
        
        fpn = path.join(fp,fn)

        if not path.exists(fpn):
            
            collectionD = self.nodeChildD['collection']
            #for item in self.nodeChildD['acquisition']:
            #    collectionD[item] = self.nodeChildD['acquisition'][item]
            for item in self.nodeChildD['classification']:
                collectionD[item] = self.nodeChildD['classification'][item]
            collectionD['dbtable'] = ''
            collectionD['dbversion'] = 'stultis001'
            collectionD['specimen'] = {}
            
            collectionD['specimen']['spruce'] = copy.deepcopy(self.nodeChildD['probesubcollection'])
            collectionD['specimen']['*'] = copy.deepcopy(self.nodeChildD['probesubcollection'])  
            collectionD['specimen']['*']['title'] = 'For all other non-spruce samples'
            collectionD['specimen']['*']['description'] = 'Specimens not given explicitly to ba captured by wildcard'
            collectionD['specimen']['*']['specimen'] = '*'
   
            with open(fpn, 'w') as outfile:
                json.dump(collectionD, outfile)
   
        # Write the collection for the endmembers
        fp = path.join(self.nodeChildD['target']['path'],'collections',
            self.nodeChildD['classification']['phylum'],
            self.nodeChildD['classification']['class'],
            'endmember','soilbrightness',
            self.nodeChildD['classification']['tractid'])
        if not path.exists(fp):
            makedirs(fp)
            
        
        fn =  '%(cid)s.json' %{'cid':self.nodeChildD['collection']['id']} 
        fpn = path.join(fp,fn)
        
        if not path.exists(fpn):

            collectionD = copy.deepcopy(self.nodeChildD['collection'])
            #for item in self.nodeChildD['acquisition']:
            #    collectionD[item] = self.nodeChildD['acquisition'][item]
                
            for item in self.nodeChildD['classification']:
                collectionD[item] = self.nodeChildD['classification'][item]
                
            collectionD['access'] = 'public'
            collectionD['metadata'] = 'public'
            collectionD['title'] = 'Soil line brightness spectral endmembers'
            collectionD['description'] = 'xspectre automatic soil line brightness retrieval'
            collectionD['class'] = 'regolith'
            collectionD['order'] = 'glaciatedsoil'
            collectionD['id'] = 'xspectre_landsat_soilline_pub' 
            #collectionD['probeinstrument'] = collectionD['spectrainstrument'] 
            
            collectionD['dbtable'] = 'aggregation'
            collectionD['dbversion'] = 'stultis001'
            
            collectionD['specimen'] = {}
            
            collectionD['specimen']['*'] = copy.deepcopy(self.nodeChildD['probesubcollection'])
            collectionD['specimen']['*']['specimen'] = '*'
  
            collectionD['specimen']['*']['title'] = 'Soil brightness and photosynthetic pigments'
            collectionD['specimen']['*']['description'] = 'xspectre automatic soil line brightness retrieval'
            collectionD['specimen']['*']['abundanceunit'] = 'None'
            collectionD['specimen']['*']['probe'] = collectionD['instrument']
            

                        
            with open(fpn, 'w') as outfile:
                json.dump(collectionD, outfile) 
    
    def WriteSample(self):
        '''
        '''
      
        for plotid in self.spectraD:
            
            #print ('spectra', plotid, self.spectraD[plotid])
            if self.spectraD[plotid]['category'] == 'annotation':
                continue
            if self.spectraD[plotid]['category'] == 'endmember':
                
                fp = path.join(self.nodeChildD['target']['path'],'samples',
                    self.nodeChildD['classification']['phylum'],
                    self.nodeChildD['classification']['class'],
                    'endmember','soilbrightness',
                    self.nodeChildD['classification']['tractid'],
                    self.nodeChildD['collection']['id'])
                if not path.exists(fp):
                    makedirs(fp)
                    
                fn = '%(p)s.json' %{'p':plotid.lower()}
                fpn = path.join(fp,fn)
                if not path.exists(fpn):
                    pass
                bandL = []
                for b in self.bandD:
                
                    bandL.append(self.spectraD[plotid]['values'][self.bandD[b]['name']])
                
                sample_id = '%(cid)s_%(sid)s_%(tract)s' %{'cid':self.nodeChildD['collection']['id'],'sid':plotid, 'tract':self.nodeChildD['classification']['tractid']}
                           
                self.spectraD[plotid]['sampleid'] = sample_id.lower()
                              
                #sample_id = 'landsatpub_%(cid)s_%(f)s' %{'cid':self.nodeChildD['collection']['id'], 'f':self.spectraD[plotid]['feature'] }
                sampleD = OrderedDict ([ ('id',sample_id), ('aggregation','xspectre_landsat_soilline_pub'),
                                    ('specimen',plotid),
                                    ('collection',self.nodeChildD['collection']['id']),
                                    ('abundance',0),
                                    ('nrspectra',1),
                                    ('spectramean',bandL),
                                    ('spectrastd',[-99 for i in bandL]),
                                    ('dbtable','endmembers'),
                                    ('dbversion','stultis001')])
                print (fpn)

                    
            else:
                fp = path.join(self.nodeChildD['target']['path'],'samples',
                    self.nodeChildD['classification']['phylum'],
                    self.nodeChildD['classification']['class'],
                    self.nodeChildD['classification']['order'],
                    self.nodeChildD['classification']['family'],
                    self.nodeChildD['classification']['tractid'],
                    self.nodeChildD['collection']['id'])
        
                if not path.exists(fp):
                    makedirs(fp)
                
                bandL = []
                for b in self.bandD:
                    bandL.append(self.spectraD[plotid]['values'][self.bandD[b]['name']])
                
                sample_id = '%(cid)s_%(f)s_%(sid)s' %{'cid':self.nodeChildD['collection']['id'],'sid':plotid, 'f':self.spectraD[plotid]['species']}
                
                self.spectraD[plotid]['sampleid'] = sample_id.lower()
                fn = '%(p)s.json' %{'p':self.spectraD[plotid]['sampleid']}
                fpn = path.join(fp,fn)
                
                sampleD = OrderedDict ([('id',sample_id),('collection',self.nodeChildD['collection']['id']),
                                    ('feature', self.spectraD[plotid]['feature']),
                                    ('specimen',self.spectraD[plotid]['species']),
                                    ('abundance',self.spectraD[plotid]['density']),
                                    ('nrspectra',1),
                                    ('spectramean',bandL),
                                    ('spectrastd',[-99 for i in bandL]),
                                    ('dbtable','samples'),
                                    ('dbversion','stultis001')])
                
                pprint(sampleD)
                
            if not path.exists(fpn):
                with open(fpn, 'w') as outfile:
                    json.dump(sampleD, outfile)
                print (fpn)
                
    def WriteSampleAuxiliary(self):
        '''
        '''

        if self.nodeChildD['classification']['siteid'] == '*':
            self.nodeChildD['classification']['siteid'] = self.nodeChildD['classification']['tractid']
        
        for plotid in self.spectraD:
            #print ('spectra', plotid, self.spectraD[plotid])
            if self.spectraD[plotid]['category'] == 'annotation':
                continue
            if self.spectraD[plotid]['category'] == 'endmember':
                continue
                
            fp = path.join(self.nodeChildD['target']['path'],'auxiliary',
                self.nodeChildD['classification']['phylum'],
                self.nodeChildD['classification']['class'],
                self.nodeChildD['classification']['order'],
                self.nodeChildD['classification']['family'],
                self.nodeChildD['classification']['tractid'],
                self.nodeChildD['collection']['id'])
    
            if not path.exists(fp):
                makedirs(fp)
            fn = '%(p)s.json' %{'p':plotid.lower()}
            fpn = path.join(fp,fn)
            #if not path.exists(fpn):
                

            sample_id = self.spectraD[plotid]['sampleid']
            fn = '%(p)s.json' %{'p':sample_id}
            fpn = path.join(fp,fn)
        
            sampleD = OrderedDict ([('id',sample_id),('collection',self.nodeChildD['collection']['id']),
                                ('slope', self.spectraD[plotid]['slope']),
                                ('aspect',-99),
                                ('elevation',-99),
                                ('soilclass','unknown'),
                                ('management','unknown'),
                                ('annualrainfall',-99),
                                ('annualevapotranspiration',-99),
                                ('USLE',-99),
                                ('dbtable','auxiliary'),
                                ('dbversion','stultis001')])
                        
            with open(fpn, 'w') as outfile:
                json.dump(sampleD, outfile)
            print (fpn)
                
    def WriteInstrument(self):
        '''
        '''

        fp = path.join(self.nodeChildD['target']['path'],'instruments',
                self.nodeChildD['spectrainstrument']['type'])
        
        if not path.exists(fp):
            makedirs(fp)
           
        fn =  '%(i)s.json' %{'i':self.nodeChildD['spectrainstrument']['instrument']} 
        
        fpn = path.join(fp,fn)

        if not path.exists(fpn):
            
            instrumentD = self.nodeChildD['spectrainstrument']
            bandL = [int(i) for i in instrumentD['bands'].split(',') ]
            instrumentD['bands'] = bandL
            bandsminL = [int(i) for i in instrumentD['bandsmin'].split(',') ]
            instrumentD['bandsmin'] = bandsminL
            bandsmaxL = [int(i) for i in instrumentD['bandsmax'].split(',') ]
            instrumentD['bandsmax'] = bandsmaxL
            bandsaliasL = [i for i in instrumentD['bandsalias'].split(',') ]
            instrumentD['bandsalias'] = bandsaliasL
            instrumentD['dbtable'] = 'instrument'
            instrumentD['dbversion'] = 'stultis001'
                                    
            with open(fpn, 'w') as outfile:
                json.dump(instrumentD, outfile)
                
    def WriteProbe(self):
        '''
        '''
        
        #<spectrainstrument instrument= 'LandsatETMreflectance' type='satelliteremotesensing'  device='NA' accuracy='0.05'  bands = '485,560,660,885,1650,2220' bandsmin = '450,520,630,770,1550,2090'  bandsmax = '520,600,690,900,1750,2350' bandsalias = 'BL,GL,RL,NA,MB,MC' metadata= 'metadata'></spectrainstrument>

        # Write the collection for the samples
        fp = path.join(self.nodeChildD['target']['path'],'probes',
                self.nodeChildD['probeinstrument']['type'])
        
        if not path.exists(fp):
            makedirs(fp)
           
        fn =  '%(i)s.json' %{'i':self.nodeChildD['probeinstrument']['probe']} 
        
        fpn = path.join(fp,fn)

        if not path.exists(fpn):
            
            probeD = self.nodeChildD['probeinstrument']

            probeD['dbtable'] = 'probe'
            probeD['dbversion'] = 'stultis001'
                                    
            with open(fpn, 'w') as outfile:
                json.dump(probeD, outfile)
 