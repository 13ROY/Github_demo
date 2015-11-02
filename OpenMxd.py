'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    NAME:       OpenMxd.py

    PURPOSE:    Python tool created for use within Arc Workflow manager to open
                an MXD dependant on the Job ID and tile number supplied.

    FUNCTIONS:
    ID      Name                                    Creator             Date
    ------  ------------------------            ----------------    ------------

    REVISIONS:
    Ver         Date        Author      Description
    ----------  ----------  ----------  ----------------------------------------
    1.0.0       11/07/2014  L Heritage  Script Creator
    ----------------------------------------------------------------------------


    VERSION CONTROL:
    To clear up any ambiguity over version number increments, the approved
    version schema is as follows:

        MAJOR:  Change IS NOT backward compatible and requires changing project
                name, path to files, GUIDs etc
        MINOR:  Change IS backward compatible. Marks introduction of new
                features
        REV:    Change IS forward/backward compatible. Revision is used for
                security/bug fixes or minimal code amendments

    The schema should be written as follows:
        MINOR.MAJOR.VER - 2.4.13

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
TOOL_VERSION = "1.0.0"
import arcpy
import os

#################################### Set Harcoded variables ##################################
# job list folder location
JobLoc = r'C:\District_50k\CheckedOutTiles'
# ArcMap file path
ArcMapPath = r'C:\Program Files (x86)\ArcGIS\Desktop10.2\bin\ArcMap.exe'

class OpenMXDTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Open An MXD"
        self.description = "Opens an MXD using the Job ID number and Tile preselected by the user. Version {0}".format(TOOL_VERSION)
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # job id parameter
    	JobID = arcpy.Parameter(
        	displayName="Job Number",
        	name="JobID",
        	datatype="String",
        	parameterType="Required",
        	direction="Input")

        # tile id parameter
    	Tile = arcpy.Parameter(
        	displayName="Tile Number",
        	name="Tile",
        	datatype="String",
        	parameterType="Required",
        	direction="Input")
        params = [JobID, Tile]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        # check if job location folder is a valid directory
        if os.path.isdir(JobLoc):
        # set the path of the tiles within the specified job
            TileLoc = os.path.join(JobLoc,'JOB_'+str(parameters[0].value))
            # if job folder does not exist, check if job folder read-only does
            if not os.path.isdir(TileLoc):
                TileLoc = os.path.join(JobLoc,'JOB_'+str(parameters[0].value)+'_Readonly')
            # if a new job is selected
            if parameters[0].altered:
                # set 'Tiles' value as a list of all the tile folders with the specified job
                parameters[1].filter.list = [tile for tile in os.listdir(TileLoc) if os.path.isdir(os.path.join(TileLoc,tile)) and len(tile) == 4]
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return


############################ START MAIN PROGRAM ##################################
    def execute(self, parameters, messages):
        """The source code of the tool."""
    # VARIABLES, PATHS, WORKSPACE
        # job folder
        jobID = 'JOB_'+str(parameters[0].value)
        # tile number
        tileID = str(parameters[1].value)
        # job folder location
        jobfdr = os.path.join(JobLoc,jobID)
        # MXD path
        MXDPath = os.path.join(jobfdr,tileID,tileID)
        # check to see if job folder is present, if not check if read-only is present
        if not os.path.isdir(jobfdr):
            MXDPath = os.path.join(jobfdr+'_Readonly',tileID,tileID)

        # check if ArcMapPath is a valid file
        if os.path.isfile(ArcMapPath):
            # check if is a valid mxd path
            if os.path.isfile(MXDPath+'.mxd'):
                # open MXD
                os.spawnv(os.P_NOWAIT, ArcMapPath, ["ArcMap.exe", MXDPath])
                arcpy.AddMessage('Opening mxd, please wait...')
            else:
                print 'Invalid mxd file path given: \t'+MXDPath
                arcpy.AddMessage('Invalid mxd file path given: \t'+MXDPath)
        else:
            print 'The harcoded ArcMap file path in the script is invalid, please change this to your current ArcMap installation path'
            arcpy.AddMessage('The harcoded ArcMap file path in the script is invalid, please change this to your current ArcMap installation path')

        return

if __name__ == '__main__':

    tool = OpenMXDTool()
    params = tool.getParameterInfo()
    tool.execute(params, None)

    pass
