# Terraform New Relic APM Entity Data Source

This module allows a New Relic application entity to be created in APM so that its ID can be used in further configuration and therefore clear a dependency on knowing the App ID for other configuration that may rely on it.

Currently both Java and Node apps are supported. When the app ID is requested the script looks up the app id from the New Relic REST API. If the app does not exist it runs a stub application that reigsters with New Relic and generates the ID. 

**Note: The apps will be created if they do not exist during a terraform PLAN**


### JAVA Setup
Build the java app first time by running the `build.sh` script in modules/app_stub/appstubs/java directory.

### Node setup
Run npm install to build the app from the modules/app_stub/appstubs/node directory.


### Usage
It is expected that you NR admin api key is already in the ENV var "NEWRELIC_API_KEY", the module will fail if not. You must specify the app's licence key as a input parameter. Call the module as follows:

```terraform
module "myModule" {
  source  = "./modules/app_stub"
  appName = "Your-App-Name"
  appType = "java"                       # "java" or "node"
  apiKey  = "YOUR-APP-API-KEY-HERE"        
}
output "JavaAppID" {
  value = module.myModule.appId          # Referernce the generated app ID like this
}
```


