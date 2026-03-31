---
name: maven-central-publish
description: Publish a Java/Kotlin library to Maven Central via Sonatype OSSRH
tool: Dev Tools
product: Maven Central
difficulty: Advanced
---

# Maven Central Publish

Publish a Java or Kotlin library to Maven Central via Sonatype's OSSRH (Open Source Software Repository Hosting).

## Tools

| Tool | Method | Docs |
|------|--------|------|
| Maven | `mvn deploy` with Sonatype plugins | https://central.sonatype.org/publish/publish-maven/ |
| Gradle | `publishToMavenCentral` with publish plugin | https://central.sonatype.org/publish/publish-gradle/ |
| Sonatype Central Portal | Web UI + API | https://central.sonatype.com/ |
| GitHub Actions | Maven/Gradle publish in CI | https://docs.github.com/en/actions/publishing-packages/publishing-java-packages-with-maven |

## Authentication

- **Sonatype account:** Register at https://central.sonatype.com/ and verify your namespace (domain or GitHub org).
- **GPG signing:** Required for Maven Central. Generate a key: `gpg --gen-key` and publish: `gpg --keyserver keyserver.ubuntu.com --send-keys <KEY_ID>`
- **CI secrets:** `MAVEN_USERNAME`, `MAVEN_PASSWORD` (Sonatype token), `GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`

## Instructions

### 1. Configure pom.xml for discoverability

```xml
<project>
  <groupId>com.yourorg</groupId>
  <artifactId>your-sdk</artifactId>
  <version>1.0.0</version>
  <name>Your SDK</name>
  <description>Verb-first description with primary keyword.</description>
  <url>https://yoursite.com/docs/sdk/java?utm_source=maven-central&amp;utm_medium=registry&amp;utm_campaign=java-sdk</url>
  <licenses>
    <license>
      <name>MIT License</name>
      <url>https://opensource.org/licenses/MIT</url>
    </license>
  </licenses>
  <scm>
    <url>https://github.com/org/java-sdk</url>
    <connection>scm:git:https://github.com/org/java-sdk.git</connection>
  </scm>
  <developers>
    <developer>
      <name>Your Name</name>
      <email>dev@yourorg.com</email>
      <organization>Your Org</organization>
    </developer>
  </developers>
</project>
```

### 2. Build, sign, and publish

```bash
# Maven
mvn clean deploy -P release

# Gradle (with central-publishing plugin)
./gradlew publishToMavenCentral --no-configuration-cache
```

### 3. Verify publication

```bash
# Check on Maven Central (indexing can take 30 minutes to 2 hours)
curl -s "https://search.maven.org/solrsearch/select?q=g:com.yourorg+AND+a:your-sdk" | python3 -m json.tool
# Visit: https://central.sonatype.com/artifact/com.yourorg/your-sdk
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Invalid Sonatype credentials | Regenerate token at central.sonatype.com |
| `GPG signature verification failed` | Key not published to keyserver | Upload key: `gpg --keyserver keyserver.ubuntu.com --send-keys <ID>` |
| `Missing required metadata` | pom.xml missing required fields | Add name, description, url, license, scm, and developer info |

## Notes

- **Maven Central is permanent:** Published versions cannot be deleted. Test with Sonatype staging first.
- **README:** Maven Central does not render README, but search.maven.org shows the pom description. Optimize the `<description>` tag.
- **Javadoc:** Maven Central requires javadoc and sources JARs. Include `-javadoc.jar` and `-sources.jar` in deployment.
