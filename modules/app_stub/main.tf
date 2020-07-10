variable "appName" {
  type = string
}
variable "apiKey" {
  type = string
  description = "New Relic API key for application reporting"
}
variable "appType" {
  type = string
  description = "'java' or 'node' application"
}

data "external" "prepareApp" {
  program = ["python3","${path.module}/prepareapp.py", var.appName, var.apiKey, var.appType]
                                        #app name    #api key    # node | java
}

output "appId" {
  value = data.external.prepareApp.result.id
}
