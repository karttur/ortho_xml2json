'''
Created on 14 Dec 2020

@author: thomasgumbricht
'''

from xml.dom import minidom
from collections import OrderedDict
from sys import exit
 
def SetModelTuning(nFeatures,nSamples,_XMLnodeChildD):
    
    testsize = _XMLnodeChildD['finalmodel']['testsize']
    nSearchSamples = nSamples*(1- testsize)
    print (nSamples,testsize, int(nSamples*(1-testsize)))

    if nSamples*(0.8) < 3:
        _XMLnodeChildD['finalmodel']['testsize'] = 0
        _XMLnodeChildD['finalmodel']['method'] = 'regr'
        _XMLnodeChildD['reflinemodel']['method'] = 'regr'
        _XMLnodeChildD['finalmodel']['folds'] = 0
        _XMLnodeChildD['reflinemodel']['folds'] = 0


    tuningD = {}
    tuningD['KnnRegr'] = {}
    tuningD['KnnRegr']["n_neighbors"] = {'min':max(1,int(nSearchSamples/4)), 'max':max(int(nSearchSamples/2),2)}
    tuningD['KnnRegr']["leaf_size"] = {'min':max(2,int(nSearchSamples/8)), 'max':max(3,int(nSearchSamples/2))}
    tuningD['KnnRegr']["weights"] = ['uniform','distance']
    tuningD['KnnRegr']["p"] = [1,2]
    tuningD['KnnRegr']["algorithm"] = ['auto','ball_tree', 'kd_tree', 'brute']
    
    tuningD['DecTreeRegr'] = {}
    tuningD['DecTreeRegr']["max_depth"] = [3, None]
    tuningD['DecTreeRegr']["min_samples_split"] = {'min':2,'max':max(3,int(nSearchSamples/2))}
    tuningD['DecTreeRegr']["min_samples_leaf"] = {'min':1,'max':max(2,int(nSearchSamples/3))}
    
    tuningD['RandForRegr'] = {}
    tuningD['RandForRegr']['max_depth'] = [3,None]
    tuningD['RandForRegr']["n_estimators"] = {'min':max(1,int(nSearchSamples/8)), 'max':max(2,int(nSearchSamples/2))}
    tuningD['RandForRegr']["max_features"] = {'min':1,'max':int(nFeatures)}
    tuningD['RandForRegr']["min_samples_split"] = {'min':2,'max':max(3,int(nSearchSamples/2))}
    tuningD['RandForRegr']["min_samples_leaf"] = {'min':1,'max':max(2,int(nSearchSamples/3))}
    tuningD['RandForRegr']["bootstrap"] = [True,False]
    
    tuningD['SVR'] = {}
    tuningD['SVR']["kernel"] = ['linear']
    tuningD['SVR']["epsilon"] = [0.1, 0.2, 0.5]
    tuningD['SVR']["C"] = [1, 3, 10]
    
    tuningD['MLP'] = {}
    tuningD['MLP']["activation"] = ['relu','identity']
    tuningD['MLP']["solver"] = ['lbfgs']
    tuningD['MLP']["hidden_layer_sizes"] = [max(3,int(nSearchSamples/2)),int(nSearchSamples),100]
    #tuningD['SVR']["C"] = [1, 3, 10]
    
    tuningD['Lasso'] = {}
    tuningD['Lasso']["alpha"] = [0.5,1.0,2.0,5.0]
    
    tuningD['LassoLars'] = {}
    tuningD['LassoLars']["alpha"] = [0.5,1.0,2.0,5.0]
    
    tuningD['Ridge'] = {}
    tuningD['Ridge']["alpha"] = [0.5,1.0,2.0,5.0]
    
    tuningD['ElasticNet'] = {}
    tuningD['ElasticNet']["alpha"] = [0.5,1.0,2.0,5.0]
    
    return tuningD
    
def SetBandOrder(bandNames, bandFiles):
    bandOrderL = ['CB','BL','GL','YL','RL','RE','NA','NB','MA','MB','MC','MD']
    bandD = OrderedDict()
    x = 0
    while True:
        nr = 0
        for band in bandOrderL:
            x += 1
            if band in bandNames:
                item = bandNames.index(band)
                bandD[nr] = {'name':band, 'file':bandFiles[item]}
                nr += 1
                continue
        if x > len(bandOrderL):
            break
    return bandD
  
def GetProcessStep(processStep):
    _rootNode = ["prep", "ini", "atcorr", "endmemb", "feature", "calib", "model", "vect", "unused", "plot", 'animate'] 
    _rootNode = ["prep", "ini", "atcorr", "parsms2json", "feature", "calib", "model", "vect", "unused", "plot", 'animate'] 

    try:
        pStep = _rootNode.index(processStep)
    except ValueError:
        print ('The initial root tag (%(s)s) is not recognized' %{'s':processStep}) 
        #TGTODO print from list
        
        exit(_rootNode)

    return pStep 
        
def ReadXMLspectra(specNode,bandD,flag):
    '''
    '''
    #set default colors for plot
    # TGOTODO GET THIS AS jsom object with default values
    outlineD = {'reference':'hotpink','calibration': 'hotpink','compare': 'hotpink', 'conflict':'crimson','constraint':'red','endmember':'black','darksoil':'DimGray','lightsoil':'LightGray','denseveg':'DarkGreen'}
    
    bandNames = []
    reflect = []
    for b in bandD:
        band = bandD[b]['name']
        bandNames.append(band)
        reflect.append(int(specNode.getAttribute(band)))
    spectra = OrderedDict(zip(bandNames, reflect)) 
    category = specNode.firstChild.nodeValue.lower()
    feature = specNode.getAttribute('feature')
    use = int(specNode.getAttribute('use'))
    


    # Properties related to drawing the spectral species
    ec = fc = lw = ls = lc = False
    text=False; rotate = 0; size = 'medium'; c = 'black'; ha = 'right'; va = 'baseline'
    font = False; style = False; weight = False;

    if specNode.hasAttribute('ec'):
        ec = specNode.getAttribute('ec')

    if specNode.hasAttribute('fc'):
        fc = specNode.getAttribute('fc')
        
    if specNode.hasAttribute('lw'):
        lw = float(specNode.getAttribute('lw'))
        
    if specNode.hasAttribute('ls'):
        ls = specNode.getAttribute('ls')

    if specNode.hasAttribute('lc'):   
        lc = specNode.getAttribute('lc')
        
    if specNode.hasAttribute('text'):   
        text = specNode.getAttribute('text')
        
    if specNode.hasAttribute('rotate'):   
        rotate = float(specNode.getAttribute('rotate'))
        
    if specNode.hasAttribute('size'):   
        size = specNode.getAttribute('size')
        
    if specNode.hasAttribute('c'):   
        c = specNode.getAttribute('c')
        
    if specNode.hasAttribute('ha'):   
        ha = specNode.getAttribute('ha')
        
    if specNode.hasAttribute('va'):   
        va = specNode.getAttribute('va')
        
    if specNode.hasAttribute('font'):   
        font = specNode.getAttribute('font')
        
    if specNode.hasAttribute('style'):   
        style = specNode.getAttribute('style')
        
    if specNode.hasAttribute('weight'):   
        weight = specNode.getAttribute('weight')
                      
    if flag:

        density = int(specNode.getAttribute('density')) 
        if specNode.getAttribute('orthoaxis') == '':
            orthoaxis = -99
        else:
            orthoaxis = int(specNode.getAttribute('orthoaxis'))  
        #Values.append([tp,ft,wt,dens,tc,spect])
        specD = OrderedDict([('feature',feature),('category', category),('orthoaxis',orthoaxis),('use',use),('density',density),('values',spectra)]) 
    else:

        specD = OrderedDict([('feature',feature),('category', category),('orthoaxis',-99),('density',False),('values',spectra)]) 
        #specD = {'category':category,'feature':feature,'weight':False,'density':False,'orthoaxis':False,'values':spectra}     
    if specNode.hasAttribute('species'):
        specD['species'] = specNode.getAttribute('species')
    if specNode.hasAttribute('slope'):
        specD['slope'] = specNode.getAttribute('slope')
    specD['ec'] = ec
    specD['fc'] = fc
    specD['lw'] = lw
    specD['ls'] = ls
    specD['lc'] = lc
    specD['text'] = text
    specD['rotate'] = rotate
    specD['size'] = size
    specD['c'] = c
    specD['ha'] = ha
    specD['va'] = va
    specD['font'] = font
    specD['style'] = style
    specD['weight'] = weight
    
    return feature, specD

def ReadGeneralXML(xmlFPN, _XMLnodeChildD):
    ''' Need to be converted to a class
    '''
 
    _spectraD = OrderedDict() 
    _emsdD = OrderedDict()
    _TCvectors = OrderedDict()
    print ('Opening XML',xmlFPN)
    dom = minidom.parse(xmlFPN)
    processStep = dom.documentElement.tagName
    _processStep = GetProcessStep(processStep)
    _XMLnodeChildD['step'] = _processStep
    #Get the parameters
    for key in _XMLnodeChildD:
        
        params = dom.getElementsByTagName(key)

        if len(params) == 0:

            pass
        else:
            for k in _XMLnodeChildD[key]: #d is a dictionary

                if k == 'node':
                    tmp = params[0].firstChild.nodeValue.lower()
 
                    if tmp == 'true':
                        _XMLnodeChildD[key][k] = True
                    else:
                        _XMLnodeChildD[key][k] = False
                    
                else:                   
                    nodeVal = params[0].getAttribute(k)
                    if len(nodeVal) > 0:
                        if type(_XMLnodeChildD[key][k]) is float:                           
                            try:
                                _XMLnodeChildD[key][k] = float(nodeVal) # update existing entry 
                            except ValueError: 
                                printstr = 'Expected a float value for tag <%(tag)s>, attribute "%(a)s"' %{'tag':key, 'a': k}
                                print (printstr)
                                exit('Please correct and restart')                           
                        elif type(_XMLnodeChildD[key][k]) is int:                            
                            try:
                                _XMLnodeChildD[key][k] = int(nodeVal) # update existing entry
                            except ValueError: 
                                printstr = 'Expected an integeter value for tag <%(tag)s>, attribute "%(a)s"' %{'tag':key, 'a': k}
                                print (printstr)
                                exit('Please correct and restart')
                        else:
                            if nodeVal.lower() == 'false':
                                _XMLnodeChildD[key][k] = False # update existing entry
                            elif nodeVal.lower() == 'true':
                                _XMLnodeChildD[key][k] = True # update existing entry
                            else:
                                _XMLnodeChildD[key][k] = nodeVal # update existing entry 
                                
    #Get the input bands and band file names and paths
    inputbands = dom.getElementsByTagName('inputbands') 
    _bandInNull = int(inputbands[0].getAttribute('null'))
    bandsIn = inputbands[0].getElementsByTagName('image') 
    bandNames = []
    bandFiles = []
    for bandIn in bandsIn:
        bandNames.append(bandIn.getAttribute('band').upper())
        bandFiles.append(bandIn.getAttribute('file'))           
    #Convert the bands to a numbered dictionary
    _bandD = SetBandOrder(bandNames, bandFiles)
    #get the spectral reference information, if not defined, just keep empty lists
    #the reference are needed for determining if optimization can be done
    #thus read before the parameters
    spectralNode = dom.getElementsByTagName('spectral')
    if len(spectralNode) > 0:
        #one at the time
        specNodes = spectralNode[0].getElementsByTagName('spectra') 
        for specNode in specNodes:
            feature, specD = ReadXMLspectra(specNode,_bandD,True)
            specD['type'] = 'spectra'
            _spectraD[feature] = specD
            #_spectraD[feature] = SetSpectra('spectra',feature,specD) 
       
    spectralsdNodes = dom.getElementsByTagName('spectralsd')
    if len(spectralsdNodes) > 0:
        #one at the time
        specsdNodes = spectralsdNodes[0].getElementsByTagName('spectra') 
        for specsdNode in specsdNodes:
            feature, specD = ReadXMLspectra(specsdNode,_bandD,False)
            specD['type'] = 'spectrasd'
            _emsdD[feature] = specD


    #read the TC parameters
    TCnode = dom.getElementsByTagName('TC')
    if TCnode:

        _TCvectors['offset'] = OrderedDict()
        _TCvectors['eigenvalues'] = OrderedDict()
        _TCvectors['features'] = OrderedDict()
        #Get the offset
        TCoffsetNode = TCnode[0].getElementsByTagName('offset')
        _TCvectors['offset']['feature'] = TCoffsetNode[0].firstChild.nodeValue
        _TCvectors['offset']['values'] = OrderedDict()
        for b in _bandD:
            band = _bandD[b]['name']
            _TCvectors['offset']['values'][band] = int(TCoffsetNode[0].getAttribute(band))
        #Get the eigenvalues
        TCvalueNodes = TCnode[0].getElementsByTagName('tcvalue')
        for TCvalueNode in TCvalueNodes:
            tcBand = TCvalueNode.getAttribute('band')
            _TCvectors['eigenvalues'][tcBand] = OrderedDict()
            _TCvectors['eigenvalues'][tcBand]['feature'] = TCvalueNode.firstChild.nodeValue
            _TCvectors['eigenvalues'][tcBand]['values'] = OrderedDict()
            for b in _bandD:
                band = _bandD[b]['name']
                _TCvectors['eigenvalues'][tcBand]['values'][band] = float(TCvalueNode.getAttribute(band))
            #params.EigenValues( tcBand, _TCvectors[tcBand] )
        #get the features
        TCfeatureNodes = TCnode[0].getElementsByTagName('tcfeature')
        for TCfeatureNode in TCfeatureNodes:
            feature = TCfeatureNode.firstChild.nodeValue
            _TCvectors['features'][feature] = OrderedDict()
            _TCvectors['features'][feature]['feature'] = TCfeatureNode.firstChild.nodeValue
            _TCvectors['features'][feature]['category'] = TCfeatureNode.getAttribute('type')
            _TCvectors['features'][feature]['weight'] = TCfeatureNode.getAttribute('weight')
            _TCvectors['features'][feature]['density'] = TCfeatureNode.getAttribute('density')
            _TCvectors['features'][feature]['values'] = OrderedDict()
            for b in _bandD:
                band = _bandD[b]['name']
                _TCvectors['features'][feature]['values'][band] = float(TCvalueNode.getAttribute(band))
            #params.TCFeature( feature, _TCvectors[feature] )
    if 'eigenvalues' in _TCvectors:
        print ('eigenvalues',_TCvectors['eigenvalues'].keys())
        
    #Get animation parameters
    anim = dom.getElementsByTagName('animation') 

    scenes = anim[0].getElementsByTagName('scene') 
    #bandNames = []
    #bandFiles = []
    sceneD = OrderedDict()

    for scene in scenes:        
        sceneD[int(scene.getAttribute('seqnr'))] = {'parameter':scene.getAttribute('parameter'),
                                                    'targetvalue':float(scene.getAttribute('targetvalue')),
                                                    'step':float(scene.getAttribute('step')),
                                                    'covtitle':scene.getAttribute('covtitle'),
                                                    'covsuptitle':scene.getAttribute('covsuptitle'),
                                                    'simtitle':scene.getAttribute('simtitle'),
                                                    'simsuptitle':scene.getAttribute('simsuptitle'),
                                                    'indtitle':scene.getAttribute('indtitle'),
                                                    'indsuptitle':scene.getAttribute('indsuptitle'),
                                                    'constraints':int(scene.getAttribute('constraints')),
                                                    'endmembers':int(scene.getAttribute('endmembers')),
                                                    'eminterpol':scene.getAttribute('eminterpol'),
                                                    'simconflicts':int(scene.getAttribute('simconflicts')),
                                                    'coninterpol':scene.getAttribute('coninterpol'),
                                                    'covconflicts':int(scene.getAttribute('covconflicts')),
                                                    'pospercent':float(scene.getAttribute('pospercent')),
                                                    'negpercent':float(scene.getAttribute('negpercent')),
                                                    'smooth':scene.getAttribute('smooth'),
                                                    'plotconflict':int(scene.getAttribute('plotconflict'))}
     
    annots = anim[0].getElementsByTagName('text')
    annotateD = OrderedDict()

    for annot in annots:        
        annotateD[int(annot.getAttribute('id'))] = {'txt':annot.getAttribute('txt'),
                                                    'cov':int(annot.getAttribute('cov')),
                                                    'sim':int(annot.getAttribute('sim')),
                                                    'ind':int(annot.getAttribute('ind')),
                                                    'startframe':int(annot.getAttribute('startframe')),
                                                    'endframe':int(annot.getAttribute('endframe')),
                                                    'x':float(annot.getAttribute('x')),
                                                    'y':float(annot.getAttribute('y')),
                                                    'xtxt':float(annot.getAttribute('xtxt')),
                                                    'ytxt':float(annot.getAttribute('ytxt')),
                                                    'color':annot.getAttribute('color'),
                                                    'font':annot.getAttribute('font'),
                                                    'size':annot.getAttribute('size'),
                                                    'style':annot.getAttribute('style'),
                                                    'weight':annot.getAttribute('weight'),
                                                    'rotation':annot.getAttribute('rotation'),
                                                    'arrow':int(annot.getAttribute('arrow')),
                                                    'fc':annot.getAttribute('fc'),
                                                    'hw':float(annot.getAttribute('hw')),
                                                    'hl':float(annot.getAttribute('hl')),
                                                    'width':float(annot.getAttribute('width')),
                                                    'linestyle':annot.getAttribute('linestyle'),
                                                    'shrink':float(annot.getAttribute('shrink'))} 
        
    samples = anim[0].getElementsByTagName('sample')
    sampleD = OrderedDict()

    for sample in samples:        
        sampleD[int(sample.getAttribute('id'))] = {'feature':sample.getAttribute('feature'),
                                                    'use':int(sample.getAttribute('use')),
                                                    'orthoaxis':int(sample.getAttribute('orthoaxis')),
                                                    'startframe':int(sample.getAttribute('startframe')),
                                                    'endframe':int(sample.getAttribute('endframe'))} 
        
        
    frames = anim[0].getElementsByTagName('frame')
    frameD = OrderedDict()

    for frame in frames: 
        pass 
        #repeat = int(frame.getAttribute('repeat') )     
        #frameD[int(sample.getAttribute('seqnr'))] = { 'repeat': repeat ),
        #                                            'transition':frame.getAttribute('transition')} 

    bandNames.append(bandIn.getAttribute('band').upper())
    bandFiles.append(bandIn.getAttribute('file'))   
        
    #Get the number of features for the final model
    nFeatures = 0
    #('ind',True),('sim',True),('cov',True),('mirrorcov',True),('mirrorsim',True),('ortho1',False),('ortho2',False),('ortho3',False),('bands',False)])
    
    if _XMLnodeChildD['finalmodel']['ind']:
        nFeatures += 1
    if _XMLnodeChildD['finalmodel']['sim']:
        nFeatures += 1
    if _XMLnodeChildD['finalmodel']['cov']:
        nFeatures += 1
   
    if  _XMLnodeChildD['domain']['Z'] == 3:
        if _XMLnodeChildD['finalmodel']['ind']:
            nFeatures += 1
        if _XMLnodeChildD['finalmodel']['sim']:
            nFeatures += 1
        if _XMLnodeChildD['finalmodel']['cov']:
            nFeatures += 1

    if  _XMLnodeChildD['finalmodel']['ortho1']:
        nFeatures += 1
    if  _XMLnodeChildD['finalmodel']['ortho2']:
        nFeatures += 1
    if  _XMLnodeChildD['finalmodel']['ortho3']:
        nFeatures += 1
    if  _XMLnodeChildD['finalmodel']['bands']:
        nFeatures += len(_bandD)

    nSamples = 0
    for item in _spectraD:
        if _spectraD[item]['category'] in ['compare','reference','calibrate','calibration']:
            nSamples += 1  
    tuningD = SetModelTuning(nFeatures,nSamples,_XMLnodeChildD)
        
    #return (xmlFPN, _XMLnodeChildD, _bandD, _processStep, _bandInNull, _spectraD, _emsdD, _TCvectors)

    #params = SetAllParams(xmlFPN, _XMLnodeChildD, _bandD, _spectraD, _emsdD, _TCvectors, tuningD)


    return (_processStep, _XMLnodeChildD, _bandInNull, _bandD, _spectraD, _emsdD, _TCvectors, tuningD, sceneD, annotateD, sampleD)

