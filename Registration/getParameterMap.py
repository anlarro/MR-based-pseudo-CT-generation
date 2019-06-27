import SimpleITK as sitk

"""Set parameters
http://elastix.bigr.nl/wiki/images/6/6e/Parameters0027_Spline_T1.txt
V. Fortunati, R.F. Verhaart, F. Angeloni, A. van der Lugt, W.J. Niessen, J.F. Veenland, M.M. Paulides and T. van Walsum, Feasibility of Multimodal
Deformable Registration for Head and Neck Tumor Treatment Planning,
Int. J. Radiation Oncology Biology and physics 90, 85-93 (2014)

Parameters file for registration taken from http://elastix.bigr.nl/wiki/index.php/Par0027
Fortunati, 2014. Feasibility of Multimodal Deformable
Registration for Head and Neck Tumor
Treatment Planning
"""

def getParameterMap():
    paramsTrans = sitk.GetDefaultParameterMap("translation")
    paramsTrans['AutomaticTransformInitialization']=["true"] ###Important to set to True

    paramsRigid = sitk.ParameterMap()
    paramsRigid['FixedInternalImagePixelType']=["float"]
    paramsRigid['MovingInternalImagePixelType']=["float"]
    paramsRigid['FixedImageDimension']=["3"]
    paramsRigid['MovingImageDimension']=["3"]

    #Main Components
    paramsRigid['UseDirectionCosines']=["true"]
    paramsRigid['Registration']=["MultiResolutionRegistration"]
    paramsRigid['Interpolator']=["BSplineInterpolator"]
    paramsRigid['ResampleInterpolator']=["FinalBSplineInterpolator"]
    paramsRigid['Resampler']=["DefaultResampler"]
    paramsRigid['FixedImagePyramid']=["FixedSmoothingImagePyramid"]
    paramsRigid['MovingImagePyramid']=["MovingSmoothingImagePyramid"]
    paramsRigid['Optimizer']=["AdaptiveStochasticGradientDescent"]
    paramsRigid['Transform']=["EulerTransform"]
    paramsRigid['Metric']=["AdvancedMattesMutualInformation"]

    paramsRigid['NumberOfResolutions']=["3"]
    paramsRigid['ImagePyramidSchedule']=["4","4","2","2","2","1","1","1","1"]

    #Transformation
    paramsRigid['AutomaticScalesEstimation']=["true"]
    paramsRigid['AutomaticTransformInitialization']=["false"]
    paramsRigid['HowToCombineTransforms']=["Compose"]

    #Optimizer
    paramsRigid['MaximumNumberOfIterations']=["500"]

    #Similarity Measure
    paramsRigid['UseNormalization']=["true"]
    paramsRigid['ErodeMask']=["false"]

    #Image sampling
    paramsRigid['NumberOfSpatialSamples']=["4000"]
    paramsRigid['ImageSampler']=["RandomCoordinate"]
    paramsRigid['NewSamplesEveryIteration']=["true"]
    paramsRigid['CheckNumberOfSamples']=["true"]

    #Interpolation and Resampling
    paramsRigid['BSplineInterpolationOrder']=["1"]
    paramsRigid['FinalBSplineInterpolationOrder']=["3"]
    paramsRigid['DefaultPixelValue']=["-1"]
    paramsRigid['WriteResultImage']=["false"]
    paramsRigid['ResultImagePixelType']=["short"]
    paramsRigid['ResultImageFormat']=["nii"]



    paramsBspline = sitk.ParameterMap()
    paramsBspline['FixedInternalImagePixelType']=["float"]
    paramsBspline['MovingInternalImagePixelType']=["float"]
    paramsBspline['FixedImageDimension']=["3"]
    paramsBspline['MovingImageDimension']=["3"]
    paramsBspline['UseDirectionCosines']=["true"]

    #Main components
    paramsBspline['Registration']=["MultiResolutionRegistration"]
    paramsBspline['Interpolator']=["BSplineInterpolator"]
    paramsBspline['ResampleInterpolator']=["FinalBSplineInterpolator"]
    paramsBspline['Resampler']=["DefaultResampler"]
    paramsBspline['FixedImagePyramid']=[ "FixedSmoothingImagePyramid"]
    paramsBspline['MovingImagePyramid']=[ "MovingSmoothingImagePyramid"]
    paramsBspline['Optimizer']=[ "AdaptiveStochasticGradientDescent"]
    paramsBspline['Transform']=[ "BSplineTransform"]
    paramsBspline['Metric']=[ "AdvancedMattesMutualInformation"]

    #Multiresolution
    paramsBspline['NumberOfResolutions']=["2"]
    paramsBspline['ImagePyramidSchedule']=["2","2","1","1","1","1"]

    #Transformation
    ###
    paramsBspline['FinalGridSpacingInPhysicalUnits']=["85"] #60
    ###
    paramsBspline['AutomaticScalesEstimation']=["true"]
    paramsBspline['AutomaticTransformInitialization']=["false"]
    paramsBspline['HowToCombineTransforms']=["Compose"]

    #Optimizer
    paramsBspline['MaximumNumberOfIterations']=["1000"]

    #Similarity measure
    paramsBspline['NumberOfHistogramBins']=["32"]
    paramsBspline['ErodeMask']=["false"]

    #Image Sampling
    paramsBspline['NumberOfSpatialSamples']=["4000"]
    paramsBspline['NewSamplesEveryIteration']=["true"]
    paramsBspline['ImageSampler']=["RandomCoordinate"]
    paramsBspline['CheckNumberOfSamples']=["true"]

    #Interpolation and Resampling
    paramsBspline['BSplineInterpolationOrder']=["1"]
    paramsBspline['FinalBSplineInterpolationOrder']=["3"]
    paramsBspline['DefaultPixelValue']=["-1"]
    paramsBspline['WriteResultImage']=["false"]
    paramsBspline['ResultImagePixelType']=["short"]
    paramsBspline['ResultImageFormat']=["nii"]


    parameterMapVector = sitk.VectorOfParameterMap()
    parameterMapVector.append(paramsTrans)
    parameterMapVector.append(paramsRigid)
    parameterMapVector.append(paramsBspline)
    # sitk.PrintParameterMap(parameterMapVector)

    return parameterMapVector