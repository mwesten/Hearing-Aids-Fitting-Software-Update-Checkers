#############################################################
#                                                           #
#                   Copyright Bluebotlabz                   #
#                                                           #
#############################################################
import html
import requests
from pathlib import Path
import libhearingdownloader
import xml.etree.ElementTree as xml


print("\n\n")
print("==================================================")
print("=        Bernafon OasisNXT Update Checker        =")
print("="*(47-len(libhearingdownloader.downloaderVersion)) + " " + libhearingdownloader.downloaderVersion + " =")

turboFile = Path("turbo.txt")
if not turboFile.is_file():
    libhearingdownloader.printWaranty()

disclaimer = [
    "DISCLAIMER",
    "",
    "The contributors of the Hearing Aids Fitting Software Update Checkers (\"The Checker\")",
    "do not take any responsability for what you do with The Checker.",
    "",
    "OasisNXT is a trademark of Bernafon",
    "Bernafon is a trademark of Oticon A/S",
    "Demant is a trademark of Demant A/S",
    "Oticon is a subsidiary of Demant A/S",
    "Oticon is a trademark of Oticon A/S",
    "OasisNXT is created by Bernafon",
    "All rights and credit go to their rightful owners. No copyright infringement intended.",
    "",
    "The contributors of The Checker, and The Checker itself are not affiliated with or endorsed by",
    "Oticon or Demant A/S",
    "Depending on how The Checker is used, it may violate the EULA and/or Terms and Conditions of the associated software.",
    "The Checker is an UNOFFICIAL project and the use of associated software may be limited."
]

# Display disclaimer
if not turboFile.is_file():
    libhearingdownloader.printDisclaimer(disclaimer)

print ("\n\nDownloading version index...")
headers = {
    "Host": "updater.bernafon.com",
    "Content-Type": "application/soap+xml; charset=utf-8"
}

updaterRetries = libhearingdownloader.updaterRetries
while updaterRetries > 0:
    try:
        # Download version data, pretending installed Oasis2 v20.22.95.0 with BernafonUpdater v27.3.26.0
        # This is required to get update for newer (2024+) versions.
        # Software names set by b:Name
        # Version numbers set by b:Major . b:Minor . b:Build . b:Revision
        rawXmlData = requests.post("https://updater.bernafon.com/UpdateWebService.svc", headers=headers, data='<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing"><s:Header><a:Action s:mustUnderstand="1">http://tempuri.org/IUpdateWebService/CheckForUpdate</a:Action><a:MessageID>urn:uuid:00000000-0000-0000-0000-000000000000</a:MessageID><a:ReplyTo><a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address></a:ReplyTo><a:To s:mustUnderstand="1">https://updater.bernafon.com/UpdateWebService.svc</a:To></s:Header><s:Body><CheckForUpdate xmlns="http://tempuri.org/"><request xmlns:b="http://schemas.datacontract.org/2004/07/Wdh.Genesis.SoftwareUpdater.Common" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><b:ClientId>00000000-0000-0000-0000-000000000000</b:ClientId><b:Languages xmlns:c="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><b:Locale>Default</b:Locale><b:Manufacturer>Bernafon</b:Manufacturer><b:OEM>Bernafon</b:OEM><b:OS>Microsoft Windows NT 10.0.22621.0</b:OS><b:RequestVersion>1</b:RequestVersion><b:Software><b:InstalledSoftware><b:Build>26</b:Build><b:Major>27</b:Major><b:Minor>3</b:Minor><b:Name>BernafonUpdater</b:Name><b:Revision>0</b:Revision></b:InstalledSoftware><b:InstalledSoftware><b:Build>95</b:Build><b:Major>20</b:Major><b:Minor>22</b:Minor><b:Name>Oasis2</b:Name><b:Revision>0</b:Revision></b:InstalledSoftware></b:Software></request></CheckForUpdate></s:Body></s:Envelope>')
        data = xml.fromstring(html.unescape(rawXmlData.text))
        break
    except:
        pass

    updaterRetries -= 1
if (updaterRetries == 0):
    print("Error: Update server could not be reached")
    exit(1)
    
packageXMLNS = '{http://www.wdh.com/xml/2012/06/25/updatemanifest.xsd}'
filesToDownload = []

if (libhearingdownloader.verboseDebug):
    print(html.unescape(rawXmlData.text))

# Get list of files
for fileData in data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "DownloadJob").find(packageXMLNS + "Files"):
    filesToDownload.append(fileData.find(packageXMLNS + "FileName").text)

# Get download server uri
downloadURI = data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "DownloadJob").find(packageXMLNS + "ServerUri").text

# Get latest version
if (libhearingdownloader.verboseDebug):
    print(data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text   + "--" +   data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Version").text)

# Define list of valid versions and their download links (direct from CDN) (predefined to online and offline of latest version)
validVersions = [
    (data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text, "The latest OasisNXT Installer (OFFLINE) (from the updater)"),
    (data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text, "The latest OasisNXT Installer (ONLINE) (from the updater)"),
]
print("\n\nThe latest available version is " + data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text + "\n\n")

if (libhearingdownloader.verboseDebug):
    print(filesToDownload)

# Select outputDir and targetVersion
outputDir = libhearingdownloader.selectOutputFolder()
targetVersion = libhearingdownloader.selectFromList(validVersions)
print("\n\n")


if (targetVersion == 0):
    outputDir += libhearingdownloader.normalizePath( data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text + "/")

    # Download and save the files
    print("Downloading " + str(len(filesToDownload)) + " files\n")
    fileIndex = 1
    for fileToDownload in filesToDownload:
        libhearingdownloader.downloadFile(downloadURI + fileToDownload, outputDir + fileToDownload, "Downloading " + fileToDownload.split("/")[-1] + " (" + str(fileIndex) + "/" + str(len(filesToDownload)) + ")")
        fileIndex += 1
elif (targetVersion == 1):
    outputDir += libhearingdownloader.normalizePath( data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text + "/")

    # Download and save the files
    fileIndex = 1
    fileToDownload = "setup.exe"
    libhearingdownloader.downloadFile(downloadURI + fileToDownload, outputDir + fileToDownload, "Downloading " + fileToDownload.split("/")[-1])

print("\n\nDownload Complete!")