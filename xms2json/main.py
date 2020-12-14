'''
Created on 14 Dec 2020

@author: thomasgumbricht
'''


from os import path, makedirs
from sys import exit
from collections import OrderedDict

from kt_xml import ReadGeneralXML
#import model.step3_v51 as STEP3
import xml2json as STEP3

from pprint import pprint

class PilotModel:
    def __init__(self, nodeChildD):
        self.nodeChildD = nodeChildD
        print (self.nodeChildD)

    def SetXMLparams(self,XMLFPN): 
        if not path.isfile(XMLFPN):
            printstr = 'The XML file %(s)s does not exist' %{'s':XMLFPN}
            exit(printstr)
        self.XMLFPN = XMLFPN
        self.XMLFP, self.XMLFN = path.split(XMLFPN)
        self. SpectralSearchXMLFPN = path.join(self.XMLFP,'spectralSearch.xml')    
        self.processStep, self.XMLnodeChildD, self.bandInNull, self.bandD, self.spectraD, self.emsdD, self.TCvectors, self.tuningD, self.sceneD, self.annotateD, self.sampleD = ReadGeneralXML(XMLFPN, _XMLnodeChildD)
          
    def ProcessStep(self):
        '''
        '''
        if self.processStep == 3:

            pprint (self.nodeChildD)
            pprint (self.bandD)
            pprint (self.spectraD)
            pprint (self.annotateD)
            pprint (self.sampleD)
            #pprint (vars(self.nodeChildD))
            step3WriteJson = STEP3.WriteJson(self.XMLFPN, self.nodeChildD,self.bandD,self.spectraD,self.tuningD, self.sceneD, self.annotateD, self.sampleD)  
                        
def GlobalLists():
    #define global lists and dictionaries
    global _XMLnodeChildD, _XMLFPN, _rootNode
    
    '''Global list for root node values to identify process steps'''
    _rootNode = ["prep", "ini", "atcorr", "endmemb", "feature", "calib", "model", "vect", "unused", "plot"]
    
    ''' Global lists, used in sub-processes, and written to intermediate XML file, including default settings '''   
    prepD = OrderedDict ([('node',False),('reference','srcwin'),('startcol',-99),('startrow',-99),('endcol',-99),('endrow',-99)])    
    iniD = OrderedDict ([('node',False),('sensor','NA'),('bandvalue','NA'),('colcomp','RLGLBL')]) 
    atmcorrD = OrderedDict ([('node',False),('sunaltitude',-99.0),('sunazimuth',-99.0),('DOY',-99),('path',False)])  
    endmemberD = OrderedDict([('node',True),('percent',1.0),('kernelsd',20),('pbimax',1000),('pbimin',200),('pvisoilmean',975),('pvisoilrange',250),('pvivegmin',1400),('ndvisoil',0),('ndvisoilrange',0.15),('errorterm','reg'),('mask','none')])   
    
    collectionD = OrderedDict([('id','collection'),('user','thomasg'),('spectradate','20101010'),('access','private'),
                    ('metadata','private'),('title','title'),('description','description'),('metaurl','#'),
                    ('measureunit','SRFI'),('instrument','LandsatETMreflectance'), ('device','NA')]) 
    
    probesubcollectionD = OrderedDict([('specimen','specimen'),('probedate','20101010'),('access','private'),
                    ('metadata','private'),('title','title'),('description','description'),('metaurl','#'),
                    ('abundanceunit','t/ha'),('probe','probe'), ('device','NA')])
    
    classificationD = OrderedDict([('phylum','landscape'),('class','vegetationcover'),('order','terrestrial'),('family','Coniferous Forests'),('tractid','CZemildata'),('siteid','*')]) 
    acquisitionD = OrderedDict([('spectradate','20101010'),
                                ('probedate','20101010') ]) 
    spectrainstrumentD = OrderedDict([('instrument','LandsatETMreflectance'),('device','device'),('type','type'),('accuracy',0.1),('bands','485, 560, 660, 885, 1650, 2220'),('bandsmin','450, 520, 630, 770, 1550, 2090'),('bandsmax','520, 600, 690, 900, 1750, 2350'), ('bandsalias','BL,GL,RL,NA,MB,MC'), ('metadata','metadata')]) 
      
    probeinstrumentD = OrderedDict([('probe','probe'),('device','device'),('type','type'),('accuracy',0.1),('metadata','metadata')]) 
        
    orthofeaturesD = OrderedDict([('node',True),('tcoffset','darksoil'),('tc1','lightsoil'),('tc2','denseveg'),('tc3','mustbeset'),('tcfeature','mustbeset')]) 
    domainD = OrderedDict([('node',True),('X',1),('Y',2),('Z',0),('logtrans',False),('exptrans',False),('fitmaxi',True)]) 

    featurelineXYD = OrderedDict([ ('node',True), ('featureXp',0), ('featureYp',0),('slope',0.0), ('intercept', 0.0), ('densitymax',0.0), ('densitymin',0.0),('maxI',0.0), ('COVoffset',0.0), ('COVrescale',0.0), ('Cfac',5000.0),('SIMfac',1.0),('r2',-9.99),('rmse',-9.99)])        

    animationD = OrderedDict([ ('node',True), ('filename', 'filename'), ('makemovie', False), ('framerate', 10) ])        

    calibrationXYD = OrderedDict([('node',True),('nsearch',3),('emsdseparate',0.0 ),('mindensity',0.0),('maxdensity',0.0),('PND',0),('SIM',0.0),('refline',0.0), ('fitem',False),('constraints',False),('includeEM',False),('r2',-9.99),('rmse',-9.99)])
    
    reflineXYD = OrderedDict([ ('node',True),('X0',0.0),('Y0',0.0),('X1',0.0),('Y1',0.0),('slope',0.0), ('intercept', 0.0), ('densitymax',0.0), ('densitymin',0.0),('maxI',0.0), ('COVoffset',0.0), ('COVrescale',0.0), ('Cfac',5000.0),('SIMconst',5000.0),('SIMfac',1.0)]) 
       
    featurelineYZD = OrderedDict([ ('node',True),('featureXp',0), ('featureYp',0),('slope',0.0), ('intercept', 0.0), ('densitymax',0.0), ('densitymin',0.0),('maxI',0.0), ('COVoffset',0.0), ('COVrescale',0.0), ('Cfac',5000.0),('SIMfac',1.0),('r2',-9.99),('rmse',-9.99)])        

    calibrationYZD = OrderedDict([('node',True),('nsearch',3),('emsdseparate',0.0 ),('mindensity',0.0),('maxdensity',0.0),('PND',0),('SIM',0.0),('refline',0.0), ('fitem',False),('constraints',False),('includeEM',False),('r2',-9.99),('rmse',-9.99)])
    
    reflineYZD = OrderedDict([ ('node',True),('X0',0.0),('Y0',0.0),('X1',0.0),('Y1',0.0),('slope',0.0), ('intercept', 0.0), ('densitymax',0.0), ('densitymin',0.0),('maxI',0.0), ('COVoffset',0.0), ('COVrescale',0.0), ('Cfac',5000.0),('SIMconst',5000.0),('SIMfac',1.0)]) 
    
    reflinemodelD = OrderedDict([('node',True),('method','regr'),('regressor','TheilSen'),('ind',True),('sim',False),('cov',False),('ortho1',False),('ortho2',False),('ortho3',False)])
    finalmodelD = OrderedDict([('node',True),('method','kfold'),('regressor','compall'),('testsize',0.3),('nTunings',6),('nIterSearch',6),('nIter',6),('folds',3),('ind',True),('sim',True),('cov',True),('ortho1',False),('ortho2',False),('ortho3',False),('bands',False)])    

    constraintsD = OrderedDict([('node',False),('endmembers',True),('eminterpol','xy'),('covconflicts',True),('coninterpol','covsim'),('simconflicts',True),('tight',False),('smooth','None'),('pospercent',100),('negpercent',100)])    
    
    plotD = OrderedDict( [('node',False),('plotcov',True), ('plotsim',True),('plotind',True), ('screen',False), ('tightlayout',True), ('singles',True),('onlyrealm',False),('onlycovsimoverlap',False), ('file',True),('xmin',-1),('ymin',-1),('xmax',-1),('ymax',-1), ('filename','filename'), ('layout','layout') ])    

    plotvectorD = OrderedDict( [('node',False),('plotcov',True), ('covlayout',''),('plotsim',True),('simlayout',''),('plotind',True),('indlayout','') ])    
 
    plotrasterD = OrderedDict( [('node',False),('plotcov',True), ('covpalette','gray'),('plotsim',True),('simpalette','gray'),('plotind',True),('indpalette','gray') ])    

    plotfeatureD = OrderedDict( [('node',True),('line',True), ('symbol',True), ('radius',-1),('tf0txt',True),('tfmaxtxt',True),('linetxt',''),('txtshift','0    '),('layout','') ] )    

    plotsampleD = OrderedDict( [('node',True),('logsize',False), ('maxize',-1), ('radius',-1),('layout','') ] )
    
    plotcalibrationD = OrderedDict( [('node',True),('logsize',False), ('maxize',-1), ('radius',-1),('layout','') ] )    

    plotvalidationD = OrderedDict( [('node',True),('logsize',False), ('maxize',-1), ('radius',-1),('layout','') ] )
    
    plotconflictD = OrderedDict( [('node',True),('layout',''), ('radius',-1) ] )
    
    plotemD = OrderedDict( [('node',True),('line',True), ('xlinetxt',''), ('ylinetxt',''),('xtxtshift',0.0),('ytxtshift',0.0),('symbol',True), ('radius',-1),('layout','') ] )    
    
    plottitleD = OrderedDict( [('node',False),('covtitle',''),('covsuptitle',''),('simtitle',''),('simsuptitle',''),('indtitle',''),('indsuptitle',''), ('layout','layout'), ('titlesize',12), ('suptitlesize',12), ('titleweight','normal'), ('suptitleweight','normal')])    

    
    intermediateD = OrderedDict([('node',True),('skipifexists',True),('stepwise',False)])
    gdalD = OrderedDict([('node',True),('path','')])
    tarD = OrderedDict([('node',False),('path',''),('plot',True),('verbose',True),('title','title')])    
    _XMLnodeChildD = OrderedDict([('prepare',prepD), ('initial',iniD), ('atmcorr',atmcorrD), ('endmembers',endmemberD), ('orthofeatures',orthofeaturesD), 
                      ('domain',domainD), 
                      ('featurelineXY',featurelineXYD), ('featurelineYZ',featurelineYZD),
                      ('collection',collectionD),('classification',classificationD),('acquisition',acquisitionD),
                      ('probesubcollection',probesubcollectionD),
                      ('spectrainstrument', spectrainstrumentD),
                      ('probeinstrument', probeinstrumentD),
                      ('animation',animationD), 
                      ('calibrationXY',calibrationXYD), ('calibrationYZ',calibrationYZD),
                      ('reflineXY',reflineXYD), ('reflineYZ',reflineYZD), 
                      ('reflinemodel',reflinemodelD),('constraints',constraintsD),
                      ('plot',plotD),('plotraster',plotrasterD),
                      ('plotvector',plotvectorD),('plotfeature',plotfeatureD),
                      ('plotsample',plotsampleD),('plotcalibration',plotcalibrationD),  
                      ('plotvalidation',plotvalidationD),('plotconflict',plotconflictD), 
                      ('plotem',plotemD),('plottitle',plottitleD), 
                      ('finalmodel',finalmodelD),('intermediates',intermediateD), ('gdalpath',gdalD), ('target',tarD) ])      
    return _XMLnodeChildD     
   
def GetEMKeys(refD):
    for key in (refD):
        if refD[key][0].lower() == 'endmember': 
            if refD[key][1].lower() == 'darksoil':
                ds = key
            if refD[key][1].lower() == 'lightsoil':
                ls = key
            if refD[key][1].lower() == 'denseveg':
                pv = key
        if 'ref' in refD[key][0].lower() and not 'max' in refD[key][1].lower() :
            ref = key 
    EMkeys = ['ds','ls','pv','ref']
    Keynr = [ds,ls,pv,ref]
    EMDict = dict(zip(EMkeys, Keynr))  
    return EMDict
        
def Initiate(XMLFPN):
    
    nodeChildD = GlobalLists()
    pilot = PilotModel(nodeChildD)
    pilot.SetXMLparams(XMLFPN)
    pilot.ProcessStep()

def SingleXML(XMLFPN):
    for f in XMLFPN:
        Initiate(f)
        
def RunFromTxtL():
    
    XMLFPN = ['/Volumes/karttur/orthomodelCZ/biomass/CZmean/Spruce-sample-1-xy/20150530-20150830/3_params2json.xml']
    SingleXML(XMLFPN)


    '''
    #txtFPN = '//Volumes/karttur2tb/orthomodelxylog/biomass/california/all.txt'
    #txtFPN = '/Volumes/karttur2tb/orthomodelxy/biomass/california/all.txt'
    #txtFPN = '/Volumes/karttur2tb/orthomodelxylog/biomass/california/plot.txt'
    #txtFPN = '//Volumes/karttur2tb/orthomodelxylog/illustration/illustration.txt'
    
    #ZC data
    txtFPN = '/Volumes/karttur/orthomodel/biomass/CZ/ZC_orthomodels.txt'
    txtFPN = '/Volumes/karttur/orthomodel/biomass/CZ/all.txt'
    txtFPN = '/Volumes/karttur/orthomodel/biomass/CZ/all-xy.txt'
    txtFPN = '/Volumes/karttur/orthomodel/biomass/CZmvc/all-yz-2014-2015.txt'
    txtFPN = '/Volumes/karttur/orthomodel/biomass/CZ-all-all-2014-2015.txt'
    #txtFPN = '/Volumes/karttur/orthomodel/biomass/CZ/rfe_yz_test.txt'
    txtFPN = '/Volumes/karttur/orthomodelCZ/biomass/all-all.txt'
    
    # Tests oct 2020
    txtFPN = '/Volumes/karttur/orthomodelCZ/biomass/Spruce-sample-1-xy.txt'
    
    with open(txtFPN) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == "#":
                continue
            XMLFPN = row[0]
            if XMLFPN[0] == "#":
                continue
            print ('XMLFPN',XMLFPN)
            Initiate(XMLFPN)    
    '''
    
if __name__ == '__main__':

    overwrite = False
    '''
    if len(sys.argv) != 2:
        sys.exit('Give the link to the XML file to run the process as the first argument')
    #Get the xml file
    XMLFPN = sys.argv[1]    
    '''
    RunFromTxtL()
    
    #SingleXML()
        