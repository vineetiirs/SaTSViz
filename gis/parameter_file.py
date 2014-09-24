##This file contains a function that reads the analysis parameters chosen by the user on the GUI and writes them in a .prm file which is read by SaTScan to start the analysis.

##Import all required files
import os
import subprocess
import shapefile

##Import required functions
from call_sat import call
from shap import make_shape 

def fill_params(file_path,time_prec,s_date,e_date,ana_type,m_type,s_area,time_agg,t_agg_len,sat_path):

    path=file_path
    path=path.split('/')
    fname=path.pop()
    path='/'.join(path)[0:]
    
    fname=fname.split('.')
    fname.reverse()
    file_name=fname.pop()
    
    fout=open(path+'/'+ file_name +'.prm','w')
    file_path_prm = path + '/'+file_name+'.prm'
    file= """ [Input]
; case data filename
CaseFile="""+ path + """/""" + file_name +""".cas
; control data filename
 ControlFile="""+ path + """/""" + file_name +""".ctl
; population data filename
PopulationFile="""+ path + """/""" + file_name +""".pop
; coordinate data filename
CoordinatesFile="""+ path +"""/"""+ file_name + """.geo
; use grid file? (y/n)
UseGridFile=n
; grid data filename
GridFile=
; time precision (0=None, 1=Year, 2=Month, 3=Day, 4=Generic)
PrecisionCaseTimes=""" + time_prec + """
; coordinate type (0=Cartesian, 1=latitude/longitude)
CoordinatesType=0
; study period start date (YYYY/MM/DD)
StartDate=""" + s_date + """
; study period end date (YYYY/MM/DD)
EndDate=""" + e_date + """

[Analysis]
; analysis type (1=Purely Spatial, 2=Purely Temporal, 3=Retrospective Space-Time, 4=Prospective Space-Time, 5=Spatial Variation in Temporal Trends, 6=Prospective Purely Temporal)
AnalysisType=""" + ana_type + """
; model type (0=Discrete Poisson, 1=Bernoulli, 2=Space-Time Permutation, 3=Ordinal, 4=Exponential, 5=Normal, 6=Continuous Poisson, 7=Multinomial)
ModelType=""" + m_type + """
; scan areas (1=High Rates(Poison,Bernoulli,STP); High Values(Ordinal,Normal); Short Survival(Exponential), 2=Low Rates(Poison,Bernoulli,STP); Low Values(Ordinal,Normal); Long Survival(Exponential), 3=Both Areas)
ScanAreas=""" + s_area + """
; time aggregation units (0=None, 1=Year, 2=Month, 3=Day, 4=Generic)
TimeAggregationUnits=""" + time_agg + """
; time aggregation length (Positive Integer)
TimeAggregationLength=""" + t_agg_len + """

[Output]
; analysis results output filename
ResultsFile="""+ path +"""/"""+ file_name +""".out.txt
; output simulated log likelihoods ratios in ASCII format? (y/n)
SaveSimLLRsASCII=n
; output simulated log likelihoods ratios in dBase format? (y/n)
SaveSimLLRsDBase=n
; output relative risks in ASCII format? (y/n)
IncludeRelativeRisksCensusAreasASCII=n
; output relative risks in dBase format? (y/n)
IncludeRelativeRisksCensusAreasDBase=n
; output location information in ASCII format? (y/n)
CensusAreasReportedClustersASCII=y
; output location information in dBase format? (y/n)
CensusAreasReportedClustersDBase=n
; output cluster information in ASCII format? (y/n)
MostLikelyClusterEachCentroidASCII=y
; output cluster information in dBase format? (y/n)
MostLikelyClusterEachCentroidDBase=n
; output cluster case information in ASCII format? (y/n)
MostLikelyClusterCaseInfoEachCentroidASCII=n
; output cluster case information in dBase format? (y/n)
MostLikelyClusterCaseInfoEachCentroidDBase=n

[Multiple Data Sets]
; multiple data sets purpose type (0=Multivariate, 1=Adjustment)
MultipleDataSetsPurposeType=0

[Data Checking]
; study period data check (0=Strict Bounds, 1=Relaxed Bounds)
StudyPeriodCheckType=0
; geographical coordinates data check (0=Strict Coordinates, 1=Relaxed Coordinates)
GeographicalCoordinatesCheckType=0

[Spatial Neighbors]
; neighbors file
NeighborsFilename=
; use neighbors file (y/n)
UseNeighborsFile=n
; meta locations file
MetaLocationsFilename=
; use meta locations file (y/n)
UseMetaLocationsFile=n
; multiple coordinates type (0=OnePerLocation, 1=AtLeastOneLocation, 2=AllLocations)
MultipleCoordinatesType=0

[Spatial Window]
; maximum spatial size in population at risk (<=50%)
MaxSpatialSizeInPopulationAtRisk=50
; maximum spatial size in max circle population file (<=50%)
MaxSpatialSizeInMaxCirclePopulationFile=50
; maximum spatial size in distance from center (positive integer)
MaxSpatialSizeInDistanceFromCenter=1
; restrict maximum spatial size - max circle file? (y/n)
UseMaxCirclePopulationFileOption=n
; restrict maximum spatial size - distance? (y/n)
UseDistanceFromCenterOption=n
; include purely temporal clusters? (y/n)
IncludePurelyTemporal=n
; maximum circle size filename
MaxCirclePopulationFile=
; window shape (0=Circular, 1=Elliptic)
SpatialWindowShapeType=0
; elliptic non-compactness penalty (0=NoPenalty, 1=MediumPenalty, 2=StrongPenalty)
NonCompactnessPenalty=0
; isotonic scan (0=Standard, 1=Monotone)
IsotonicScan=0

[Temporal Window]
; maximum temporal cluster size (<=90%)
MaxTemporalSize=50
; include purely spatial clusters? (y/n)
IncludePurelySpatial=n
; how max temporal size should be interpretted (0=Percentage, 1=Time)
MaxTemporalSizeInterpretation=0
; temporal clusters evaluated (0=All, 1=Alive, 2=Flexible Window)
IncludeClusters=0
; flexible temporal window start range (YYYY/MM/DD,YYYY/MM/DD)
IntervalStartRange=2000/1/1,2000/12/31
; flexible temporal window end range (YYYY/MM/DD,YYYY/MM/DD)
IntervalEndRange=2000/1/1,2000/12/31

[Space and Time Adjustments]
; time trend adjustment type (0=None, 1=Nonparametric, 2=LogLinearPercentage, 3=CalculatedLogLinearPercentage, 4=TimeStratifiedRandomization, 5=CalculatedQuadraticPercentage)
TimeTrendAdjustmentType=0
; time trend adjustment percentage (>-100)
TimeTrendPercentage=0
; adjustments by known relative risks file name (with HA Randomization=1)
AdjustmentsByKnownRelativeRisksFilename=
; use adjustments by known relative risks file? (y/n)
UseAdjustmentsByRRFile=n
; spatial adjustments type (0=No Spatial Adjustment, 1=Spatially Stratified Randomization)
SpatialAdjustmentType=0
; time trend type - SVTT only (Linear=0, Quadratic=1)
TimeTrendType=0

[Inference]
; prospective surveillance start date (YYYY/MM/DD)
ProspectiveStartDate=2000/12/31
; p-value reporting type (Default p-value=0, Standard Monte Carlo=1, Early Termination=2, Gumbel p-value=3) 
PValueReportType=0
; report Gumbel p-values
ReportGumbel=n
; early termination threshold
EarlyTerminationThreshold=50
; adjust for earlier analyses(prospective analyses only)? (y/n)
AdjustForEarlierAnalyses=n
; perform iterative scans? (y/n)
IterativeScan=n
; maximum iterations for iterative scan (0-32000)
IterativeScanMaxIterations=10
; max p-value for iterative scan before cutoff (0.000-1.000)
IterativeScanMaxPValue=0.05
; Monte Carlo replications (0, 9, 999, n999)
MonteCarloReps=999

[Clusters Reported]
; criteria for reporting secondary clusters(0=NoGeoOverlap, 1=NoCentersInOther, 2=NoCentersInMostLikely,  3=NoCentersInLessLikely, 4=NoPairsCentersEachOther, 5=NoRestrictions)
CriteriaForReportingSecondaryClusters=0
; restrict reported clusters to maximum geographical cluster size? (y/n)
UseReportOnlySmallerClusters=n
; maximum reported spatial size in population at risk (<=50%)
MaxSpatialSizeInPopulationAtRisk_Reported=50
; maximum reported spatial size in max circle population file (<=50%)
MaxSizeInMaxCirclePopulationFile_Reported=50
; maximum reported spatial size in distance from center {positive integer)
MaxSpatialSizeInDistanceFromCenter_Reported=1
; restrict maximum reported spatial size - max circle file? (y/n)
UseMaxCirclePopulationFileOption_Reported=n
; restrict maximum reported spatial size - distance? (y/n)
UseDistanceFromCenterOption_Reported=n

[Additional Output]
; report critical values for .01 and .05? (y/n)
CriticalValue=n
; report cluster rank (y/n)
ReportClusterRank=n
; print ascii headers in output files (y/n)
PrintAsciiColumnHeaders=n

[Elliptic Scan]
; elliptic shapes - one value for each ellipse (comma separated decimal values)
EllipseShapes=1.5,2,3,4,5
; elliptic angles - one value for each ellipse (comma separated integer values)
EllipseAngles=4,6,9,12,15

[Power Simulations]
; p-values for 2 pre-specified log likelihood ratios? (y/n)
PValues2PrespecifiedLLRs=n
; power calculation log likelihood ratio (no. 1)
LLR1=0
; power calculation log likelihood ratio (no. 2)
LLR2=0
; simulation methods (0=Null Randomization, 1=HA Randomization, 2=File Import)
SimulatedDataMethodType=0
; simulation data input file name (with File Import=2)
SimulatedDataInputFilename=
; print simulation data to file? (y/n)
PrintSimulatedDataToFile=n
; simulation data output filename
SimulatedDataOutputFilename=

[Run Options]
; analysis execution method  (0=Automatic, 1=Successively, 2=Centrically)
ExecutionType=0
; number of parallel processes to execute (0=All Processors, x=At Most X Processors)
NumberParallelProcesses=0
; log analysis run to history file? (y/n)
LogRunToHistoryFile=n
; suppressing warnings? (y/n)
SuppressWarnings=n

[System]
; system setting - do not modify
Version=9.0.1"""
    fout.write(file)
    fout.close()
    
    out_file=path +"\\"+ file_name + ".out.txt"
    list1=[file_path_prm,out_file,sat_path,path,file_name,path+'\\'+file_name+'_cluster.shp',file_name+'_cluster']
    return list1

