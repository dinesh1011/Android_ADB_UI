
var app = angular.module('adbInstallation', []);

//as python jinga uses double braces its not working with template so changing the interpolate provided to double slash
app.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//').endSymbol('//');
    });

//all app controller activiteis goes here
app.controller('installationController', function($scope, $http) {
    $scope.selectpackage = {};
    $scope.name = "John Doe";
    $scope.sel = "saab";
    $scope.testdata = "Dinesh-test";
    $scope.selectfile = {};
    $scope.fileInput = "";
    $scope.requestProgress = {};

//get devices connected - http get request
    $http({method:'GET', url:'get_devices'})
    .then(function successCallback(data, status, headers, config) {
        $scope.connectedDevices = data.data;
        $scope.deviceAvailability = (Object.keys(data.data).length);
        if(angular.equals({}, data.data)){
            $scope.deviceMessage = " No devices available to display";  }
        //console.log(data.data);
    }, function errorCallback(response) {
        console.log("Fail");
    });

//get packages - http get request
    $scope.refreshPackages = getPackages;
    function getPackages(){
        $scope.packageList = {};
        $http({method:'GET', url:'get_installed_packages'})
        .then(function successCallback(data, status, headers, config) {
            var deviceobj = data.data;
            $scope.packageList = deviceobj
            $scope.packageTable = Object.keys(deviceobj).length;
            if(angular.equals({}, deviceobj)){ $scope.packageMessage = "No Packages available to display"; }
        }, function errorCallback(response) {
            console.log("Fail");
        });
    }
    getPackages();

//uninstall selected packages from respective devices - collect data
    var dataobjectPackages = {};
    $scope.uninstall = function(){
        var deviceId;
        angular.forEach($scope.selectpackage, function(item, key){
            var packages = [];
            deviceId = key;
            angular.forEach(item, function(itemval, key){
                if(itemval){
                    //console.log(itemval);
                    packages.push(key); }
            });

            if(packages.length){
            dataobjectPackages[deviceId] =  packages; }
        });

        if(Object.keys(dataobjectPackages).length){
            requestUninstall();
            $scope.selectpackage = {};  }
        else{ alert("please select packages");  }
    }

//uninstall post request
function requestUninstall(){
    var request = {
        method: 'POST',
        url: 'uninstall_packages',
        data: dataobjectPackages,
        headers: {'Content-Type': 'application/json'}  };
        $http(request)
        .then(function successCallback(data, status, headers, config) {
            console.log(JSON.stringify(data.data));
            alert(JSON.stringify(data.data));
        }, function errorCallback(data, status, headers, config) {
            alert(data.data);
        });
    dataobjectPackages = null;
    dataobjectPackages = {};
}

//on input file change clear selection check box values
$scope.fileChange = function(){
    $scope.selectfile = {};
    $scope.requestProgress = {};
}

//install selected packages in respective devices - collect data
    var dataobjectInstallPackages = {};
    $scope.install = function(){
        var deviceId;
        angular.forEach($scope.selectfile, function(item, key){
            var packageUrls = "";
            deviceId = key;
            angular.forEach(item, function(itemval, key){
                if(itemval){
                    //console.log(itemval);
                    packageUrls = key; }
            });

            if(packageUrls != ""){
            dataobjectInstallPackages[deviceId] =  packageUrls; }
        });
        //console.log(dataobjectInstallPackages);
        if(Object.keys(dataobjectInstallPackages).length){
            requestInstall();
            $scope.selectfile = {};  }
        else{ alert("please select packages");  }
    }




    //install selected packages in respective devices - collect data - and iterate requests
        var dataobjectInstallPackagesIter = {};
        var dataobjectInstallPackagesIterEach = {};
        $scope.installOneByOne = function(){
            var deviceId;
            angular.forEach($scope.selectfile, function(item, key){
                var packageUrls = "";
                deviceId = key;
                angular.forEach(item, function(itemval, key){
                    if(itemval){
                        console.log(itemval);
                        packageUrls = key; }
                });

                if(packageUrls){
                dataobjectInstallPackagesIter[deviceId] =  packageUrls; }
            });
            //console.log(dataobjectInstallPackages);
            if(Object.keys(dataobjectInstallPackagesIter).length){
                angular.forEach(dataobjectInstallPackagesIter, function(item, key){
                    dataobjectInstallPackagesIterEach[key] = item;
                    requestInstall(key);
                    //console.log(dataobjectInstallPackagesIter);
                    //console.log(dataobjectInstallPackagesIterEach);
                    dataobjectInstallPackagesIterEach = null;
                    dataobjectInstallPackagesIterEach = {};
                })
                //requestInstall();
                $scope.selectfile = {};
                dataobjectInstallPackagesIter = null;
                dataobjectInstallPackagesIter = {}; }
            else{ alert("please select packages");  }
        }


    //install post request
    function requestInstall(deviceId){
        var request = {
            method: 'POST',
            url: 'install_packages',
            data: dataobjectInstallPackagesIterEach,
            headers: {'Content-Type': 'application/json'}  };
            $scope.requestProgress[deviceId] = "Req. Processing";
            $http(request)
            .then(function successCallback(data, status, headers, config) {
                //console.log(JSON.stringify(data.data));
                alert(JSON.stringify(data.data));
                $scope.requestProgress[deviceId] = data.status;
                //console.log(data.status);
            }, function errorCallback(data, status, headers, config) {
                alert(data.data);
                $scope.requestProgress[deviceId] = data.status;
            });
        dataobjectInstallPackagesIterEach = null;
        dataobjectInstallPackagesIterEach = {};
    }

//app controller ends
});
