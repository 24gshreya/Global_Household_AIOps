@description('Existing Foundry account name')
param foundryName string

@description('Deployment name')
param deploymentName string

@description('Model name')
param modelName string

@description('Model publisher/format')
param modelFormat string

@description('Model version')
param modelVersion string

@description('Deployment SKU')
param skuName string

@description('Deployment capacity')
param capacity int

resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: foundryName
}

resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-04-01-preview' = {
  parent: foundry
  name: deploymentName

  sku: {
    name: skuName
    capacity: capacity
  }

  properties: {
    model: {
      format: modelFormat
      name: modelName
      version: modelVersion
    }
  }
}

output deploymentName string = modelDeployment.name
output deploymentId string = modelDeployment.id
