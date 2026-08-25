@description('Azure deployment region')
param location string

@description('Microsoft Foundry resource name')
param foundryName string

@description('Microsoft Foundry project name')
param projectName string

resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: foundryName
  location: location
  kind: 'AIServices'

  sku: {
    name: 'S0'
  }

  identity: {
    type: 'SystemAssigned'
  }

  properties: {
    customSubDomainName: foundryName
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
    allowProjectManagement: true
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: foundry
  name: projectName
  location: location

  identity: {
    type: 'SystemAssigned'
  }

  properties: {}
}

output foundryId string = foundry.id
output foundryName string = foundry.name
output projectId string = project.id
output projectName string = project.name
