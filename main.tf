# Just an example of how to call the module for each app type


# === Example node app creation ===
module "nodeApp" {
  source  = "./modules/app_stub"
  appName = "ExampleNodeApp1"
  appType = "node"
  apiKey  = "APP-API-KEY-HERE"
}

output "NodeAppID" {
  value = module.nodeApp.appId
}



# === Example java app creation ===
module "javaApp" {
  source  = "./modules/app_stub"
  appName = "ExampleJavaApp1"
  appType = "java"
  apiKey  = "APP-API-KEY-HERE"
}
output "JavaAppID" {
  value = module.javaApp.appId
}

