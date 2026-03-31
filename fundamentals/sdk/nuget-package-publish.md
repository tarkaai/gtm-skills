---
name: nuget-package-publish
description: Publish or update a .NET package on NuGet.org with metadata optimized for discoverability
tool: dotnet CLI / NuGet API
difficulty: Setup
---

# NuGet Package Publish

Publish a .NET package to NuGet.org with metadata configured for developer discoverability.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| dotnet CLI | `dotnet nuget push` | https://learn.microsoft.com/en-us/nuget/nuget-org/publish-a-package |
| NuGet CLI | `nuget push` | https://learn.microsoft.com/en-us/nuget/reference/cli-reference/cli-ref-push |
| GitHub Actions | `dotnet nuget push` in CI | https://docs.github.com/en/actions/publishing-packages/publishing-nuget-packages |
| Azure DevOps | `NuGetCommand@2` task | https://learn.microsoft.com/en-us/azure/devops/pipelines/artifacts/nuget |

## Authentication

- **dotnet CLI:** Pass API key via `--api-key`. Create at https://www.nuget.org/account/apikeys
- **CI:** Store key as `NUGET_API_KEY` secret. Scope to specific packages and allow push only.

## Instructions

### 1. Configure .csproj for discoverability

```xml
<PropertyGroup>
  <PackageId>YourOrg.PackageName</PackageId>
  <Version>1.0.0</Version>
  <Description>Verb-first description with primary keyword.</Description>
  <PackageTags>keyword1;keyword2;keyword3;keyword4</PackageTags>
  <PackageProjectUrl>https://yoursite.com/docs/sdk/dotnet?utm_source=nuget&amp;utm_medium=registry&amp;utm_campaign=dotnet-sdk</PackageProjectUrl>
  <RepositoryUrl>https://github.com/org/dotnet-sdk</RepositoryUrl>
  <PackageLicenseExpression>MIT</PackageLicenseExpression>
  <PackageReadmeFile>README.md</PackageReadmeFile>
</PropertyGroup>
<ItemGroup>
  <None Include="README.md" Pack="true" PackagePath="\" />
</ItemGroup>
```

### 2. Build and publish

```bash
dotnet pack --configuration Release
dotnet nuget push ./bin/Release/YourOrg.PackageName.1.0.0.nupkg \
  --api-key $NUGET_API_KEY \
  --source https://api.nuget.org/v3/index.json
```

### 3. Verify publication

```bash
# NuGet packages can take up to 30 minutes to index
dotnet nuget search YourOrg.PackageName --source https://api.nuget.org/v3/index.json
# Visit: https://www.nuget.org/packages/YourOrg.PackageName
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Forbidden` | API key lacks push scope | Create a new key with push permissions for this package |
| `409 Conflict` | Version already exists | Bump version in .csproj |
| `400 Bad Request` | Invalid package metadata | Run `dotnet pack` and fix validation errors |

## Notes

- **README on NuGet:** NuGet renders the included README.md on the package page. Include CTA with `utm_source=nuget`.
- **Unlisting:** To hide a version from search (but allow direct install): `dotnet nuget delete YourOrg.PackageName 1.0.0 --source https://api.nuget.org/v3/index.json`
