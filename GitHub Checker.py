import os
import datetime
import requests
import json
import libhearingdownloader

updaterRetries = libhearingdownloader.updaterRetries
while updaterRetries > 0:
    try:
        rawJsonData = requests.get("https://api.github.com/repos/JediLin/Hearing-Aids-Fitting-Software-Update-Checkers/releases/latest")
        data = json.loads(rawJsonData.text)
        break
    except:
        pass

    updaterRetries -= 1
if (updaterRetries == 0):
    print("Error: Update server could not be reached")
    exit(1)

if (libhearingdownloader.verboseDebug):
    print(rawJsonData.text)

print("\n\nThe latest available version is " + data['tag_name'])
print("\nYou are using " + libhearingdownloader.downloaderVersion + "\n")

if (data['tag_name'] == libhearingdownloader.downloaderVersion):
    print("No update available.\n")
    # exit(1)

print("You can download the latest release version, or the pre-release work-in-progress version AT YOUR OWN RISK!\n")

availableFiles = [] # List of available files
availableFiles.append( (data['tag_name'], os.path.basename(data['assets'][0]['browser_download_url']), data['assets'][0]['browser_download_url']) )
currentTime = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y%m%d%H%M')
wipName = "Hearing-Aids-Fitting-Software-Update-Checkers-WIP-" + currentTime + ".zip"
availableFiles.append( ("Pre-release WIP", os.path.basename(wipName), "https://github.com/JediLin/Hearing-Aids-Fitting-Software-Update-Checkers/archive/main.zip") )

if (libhearingdownloader.verboseDebug):
    print(availableFiles)

# Select outputDir and targetFile
outputDir = libhearingdownloader.selectOutputFolder()
targetFile = availableFiles[libhearingdownloader.selectFromList(availableFiles)]

# Create download folder
downloadVer = 'Update Checker ' + targetFile[0]
outputDir += '.'.join(downloadVer.split('.')) + "/"
print("\n\n")

# Download file
libhearingdownloader.downloadFile(targetFile[2], outputDir + targetFile[1], "Downloading " + targetFile[1])

print("\n\nDownload Complete!")
