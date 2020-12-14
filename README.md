## ortho_xml2json

Python package that converts xml written for Karttur's ortho-model into json.

```
<?xml version='1.0' encoding='utf-8'?>
<feature>
    <prepare reference="srcwin" startcol="-99" startrow="-99" endcol="-99" endrow="-99">False</prepare>
    <initial sensor="NA" bandvalue="NA" colcomp="RLGLBL">False</initial>
    <atmcorr sunaltitude="-99.0" sunazimuth="-99.0" DOY="-99" path="False">False</atmcorr>
    <endmembers percent="1.0" kernelsd="20" pbimax="1000" pbimin="200" pvisoilmean="975" pvisoilrange="250" pvivegmin="1400" ndvisoil="0" ndvisoilrange="0.15" errorterm="reg" mask="none">True</endmembers>
    <orthofeatures tcoffset="darksoil" tc1="lightsoil" tc2="denseveg" tc3="1412_CZ" tcfeature="1412_CZ">True</orthofeatures>
    <domain X="1" Y="2" Z="0" logtrans="True" exptrans="False" fitmaxi="False">True</domain>
    <featurelineXY featureXp="0" featureYp="0" slope="0.0" intercept="0.0" densitymax="318.420584" densitymin="0.0" maxI="0.0" COVoffset="0.0" COVrescale="0.0" Cfac="5000.0" SIMfac="1.0" r2="-9.99" rmse="-9.99">True</featurelineXY>
    <featurelineYZ featureXp="0" featureYp="0" slope="0.0" intercept="0.0" densitymax="318.420584" densitymin="0.0" maxI="0.0" COVoffset="0.0" COVrescale="0.0" Cfac="5000.0" SIMfac="1.0" r2="-9.99" rmse="-9.99">True</featurelineYZ>
    <calibrationXY nsearch="3" emsdseparate="0.0" mindensity="10.0" maxdensity="10.0" PND="20" SIM="1.0" refline="10.0" fitem="False" constraints="False" includeEM="False" r2="-9.99" rmse="-9.99" Cfac="5000">True</calibrationXY>
    <calibrationYZ nsearch="3" emsdseparate="0.0" mindensity="10.0" maxdensity="10.0" PND="10" SIM="1.0" refline="10.0" fitem="False" constraints="False" includeEM="False" r2="-9.99" rmse="-9.99" Cfac="5000">True</calibrationYZ>
    <reflineXY X0="0.0" Y0="0.0" X1="0.0" Y1="0.0" slope="0.0" intercept="0.0" densitymax="0.0" densitymin="0.0" maxI="0.0" COVoffset="0.0" COVrescale="0.0" Cfac="5000.0" SIMconst="5000.0" SIMfac="1.0">True</reflineXY>
    <reflineYZ X0="0.0" Y0="0.0" X1="0.0" Y1="0.0" slope="0.0" intercept="0.0" densitymax="0.0" densitymin="0.0" maxI="0.0" COVoffset="0.0" COVrescale="0.0" Cfac="5000.0" SIMconst="5000.0" SIMfac="1.0">True</reflineYZ>
    <reflinemodel method="regr" regressor="TheilSen" ind="True" sim="False" cov="False" ortho1="False" ortho2="False" ortho3="False">True</reflinemodel>
    <finalmodel method="kfold" regressor="compall" testsize="0.3" nTunings="6" nIterSearch="6" nIter="6" folds="3" ind="True" sim="True" cov="True" ortho1="False" ortho2="False" ortho3="False" bands="False">True</finalmodel>
    <intermediates skipifexists="True" stepwise="False">True</intermediates>
    <gdalpath path="">True</gdalpath>
    <target path="/Volumes/karttur/orthomodelCZ/biomass/CZmean/Oak-sample-1-xy/20150530-20150830" plot="True" verbose="True" title="Oak-sample-1-xy">False</target>
    <inputbands null="-9999">
         <image band = "BL" file = ""></image>
         <image band = "GL" file = ""></image>
         <image band = "RL" file = ""></image>
         <image band = "NA" file = ""></image>
         <image band = "MB" file = ""></image>
         <image band = "MC" file = ""></image>
    </inputbands>
    <spectral>
        <spectra feature = "darksoil" orthoaxis =  "0" weight = "0"  density = "0"  MC = "193" MB = "308" BL = "212" NA = "696" RL = "237" GL = "302">endmember</spectra>
        <spectra feature = "lightsoil" orthoaxis =  "1" weight = "0"  density = "0"  MC = "1519" MB = "1918" BL = "704" NA = "1785" RL = "1164" GL = "988">endmember</spectra>
        <spectra feature = "denseveg" orthoaxis =  "2" weight = "0"  density = "0"  MC = "809" MB = "1968" BL = "211" NA = "6438" RL = "299" GL = "606">endmember</spectra>
        <spectra species = "oak" feature = "1412_CZ" orthoaxis =  "3"  slope = "0.0"  density = "318"  MC = "548" MB = "1393" BL = "218" NA = "3413" RL = "248" GL = "356">reference</spectra>
    </spectral>
</feature>
```
