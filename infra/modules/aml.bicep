@description('Azure deployment region')
param location string

@description('Azure ML workspace name')
param workspaceName string

@description('Storage account name')
param storageAccountName string

@description('Key Vault name')
param keyVaultName string

@description('Existing Application Insights resource ID')
param applicationInsightsId string


resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location

  sku: {
    name: 'Standard_LRS'
  }

  kind: 'StorageV2'

  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    publicNetworkAccess: 'Enabled'
  }
}


resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location

  properties: {
    tenantId: tenant().tenantId

    sku: {
      family: 'A'
      name: 'standard'
    }

    enableRbacAuthorization: true
    enableSoftDelete: true
    publicNetworkAccess: 'Enabled'
  }
}


resource amlWorkspace 'Microsoft.MachineLearningServices/workspaces@2025-12-01' = {
  name: workspaceName
  location: location

  identity: {
    type: 'SystemAssigned'
  }

  sku: {
    name: 'Basic'
    tier: 'Basic'
  }

  kind: 'Default'

  properties: {
    storageAccount: storage.id
    keyVault: keyVault.id
    applicationInsights: applicationInsightsId

    publicNetworkAccess: 'Enabled'
    v1LegacyMode: false
  }
}


output workspaceName string = amlWorkspace.name
output workspaceId string = amlWorkspace.id
output storageAccountName string = storage.name
output keyVaultName string = keyVault.name
