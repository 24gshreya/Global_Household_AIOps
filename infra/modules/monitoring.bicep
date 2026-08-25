@description('Azure deployment region')
param location string

@description('Log Analytics workspace name')
param logAnalyticsName string

@description('Application Insights resource name')
param appInsightsName string

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location

  properties: {
    retentionInDays: 30
  }
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'

  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

output logAnalyticsId string = logAnalytics.id
output applicationInsightsId string = applicationInsights.id
output applicationInsightsName string = applicationInsights.name