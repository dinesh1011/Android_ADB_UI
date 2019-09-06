from sanic import Sanic
from sanic import response
#from sanic_jinja2 import SanicJinja2
import adbinstall as adb_install
import json
import asyncio
import concurrent.futures
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import os
import sys

executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

app = Sanic(__name__)
#app.config.RESPONSE_TIMEOUT = 180
app.config.REQUEST_TIMEOUT = 180
#app.config.KEEP_ALIVE = True
#app.config.KEEP_ALIVE_TIMEOUT = 60
exePath = os.path.dirname(os.path.realpath(sys.argv[0]))
app.static("static", exePath + "/static")
#jinja = SanicJinja2(app)

"""@app.route("/")
async def mainpage(request):
    return jinja.render('index.html', request, greetings='Hello, sanic!')
    #return response.text(os.getcwd())"""

def template(tpl, **kwargs):
    env = Environment(loader = FileSystemLoader(exePath + '/static/templates'),autoescape=select_autoescape(['html', 'xml', 'tpl']))
    template = env.get_template(tpl)
    return response.html(template.render(kwargs))

@app.route('/')
async def index(request):
    return template('index.html')

@app.route("/get_devices")
async def getPackages(request):
    connectedDevices = adb_install.get_devices()
    #connectedDevices = """<!doctype html><html><head><meta charset=\"UTF-8\"><title>demo1</title><link href=\"../static/css/demo.css\" rel=\"stylesheet\"  type=\"text/css\"></head><body class=\"bodymain\"><h1>ADB Anstallation App</h1><div class=\"getdevices\">  <h2>Connected devices: </h2>  <table  width=\"200\" border=\"1\" class=\"devices\">    <tbody>      <tr><td>Device Id </td>        <td> Device Name</td>      </tr>      <tr><td>&nbsp;</td>        <td>&nbsp;</td>      </tr>      <tr><td>&nbsp;</td>        <td>&nbsp;</td>      </tr>    </tbody>  </table></div></body></html>"""
    return response.json(connectedDevices)

@app.route("/get_installed_packages")
async def getInstalledPackages(request):
    loop = asyncio.get_event_loop()
    devices = adb_install.get_devices()
    packagesdata = {}
    for device in devices:
        apps = await loop.run_in_executor(executor, adb_install.get_installed_packages, device)
        packagesdata[device] = apps
    return response.json(packagesdata)

@app.route("/uninstall_packages", methods=["POST"])
async def uninstallPackages(request):
    loop = asyncio.get_event_loop()
    requestJson = json.loads(request.body)
    responseJson = {}
    for device, packages in requestJson.items():
        print(device, packages)
        responseText = await loop.run_in_executor(executor, adb_install.uninstall_package, device, packages)
        responseJson[device] = responseText
    return response.json(responseJson)

@app.route("/install_package_dax", methods=["POST"])
async def installPackageDax(request):
    loop = asyncio.get_event_loop()
    requestJson = json.loads(request.body)
    responseJson = {}
    for device, deviceId in requestJson.items():
        print(device, deviceId)
        responseText = await loop.run_in_executor(executor, adb_install.install_package, deviceId, "DAX")
        responseJson[deviceId] =  responseText
    return response.json(responseJson)

@app.route("/install_packages", methods=["POST"])
async def installPackages(request):
    loop = asyncio.get_event_loop()
    requestJson = json.loads(request.body)
    responseJson = {}
    for deviceId, packageUrls in requestJson.items():
        print(deviceId, packageUrls)
        responseText = await loop.run_in_executor(executor, adb_install.install_packages, deviceId, packageUrls)
        responseJson[deviceId] =  responseText
    return response.json(responseJson)


@app.route("/install_package_pax", methods=["POST"])
async def installPackagePax(request):
    loop = asyncio.get_event_loop()
    requestJson = json.loads(request.body)
    responseText = ""
    for device, deviceId in requestJson.items():
        print(device, deviceId)
        responseText = await loop.run_in_executor(executor, adb_install.install_package, deviceId, "PAX")
        responseText =  responseText.decode("UTF-8")
    return response.text(responseText)

app.run(host="localhost", port=8080, debug=True)
