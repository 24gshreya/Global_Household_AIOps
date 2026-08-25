targetScope = 'resourceGroup'

@description('Azure region')
param location string = resourceGroup().location

@description('Prefix used for resource naming')
param prefix string = 'ghaiops'

var uniqueSuffix = substring(
  uniqueString(resourceGroup().id),
  0,
  6
)

var foundryName = '${prefix}-foundry-${uniqueSuffix}'
var projectName = '${prefix}-project'
var logAnalyticsName = '${prefix}-logs-${uniqueSuffix}'
var appInsightsName = '${prefix}-appi-${uniqueSuffix}'
var amlWorkspaceName = '${prefix}-mlw-${uniqueSuffix}'
var amlStorageName = replace('${prefix}ml${uniqueSuffix}','-','')
var amlKeyVaultName = '${prefix}-kv-${uniqueSuffix}'

module monitoring './modules/monitoring.bicep' = {
  name: 'monitoringDeployment'

  params: {
    location: location
    logAnalyticsName: logAnalyticsName
    appInsightsName: appInsightsName
  }
}

module foundry './modules/foundry.bicep' = {
  name: 'foundryDeployment'

  params: {
    location: location
    foundryName: foundryName
    projectName: projectName
  }
}

module modelDeployment './modules/model-deployment.bicep' = {
  name: 'modelDeployment'

  params: {
    foundryName: foundry.outputs.foundryName
    deploymentName: 'gpt-5-mini-demo'
    modelName: 'gpt-5-mini'
    modelFormat: 'OpenAI'
    modelVersion: '2025-08-07'
    skuName: 'GlobalStandard'
    capacity: 10
  }
}

module aml './modules/aml.bicep' = {
  name: 'amlDeployment'

  params: {
    location: location
    workspaceName: amlWorkspaceName
    storageAccountName: amlStorageName
    keyVaultName: amlKeyVaultName
    applicationInsightsId:monitoring.outputs.applicationInsightsId
  }
}

output foundryName string = foundry.outputs.foundryName
output foundryProjectName string = foundry.outputs.projectName
output appInsightsName string = monitoring.outputs.applicationInsightsName
output appInsightsId string = monitoring.outputs.applicationInsightsId
output modelDeploymentName string = modelDeployment.outputs.deploymentName
output amlWorkspaceName string = aml.outputs.workspaceName
