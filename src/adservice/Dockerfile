# Use a non-Alpine builder to avoid Java SSL issues
FROM eclipse-temurin:21.0.5_11-jdk AS builder

WORKDIR /app

# Leverage Docker build cache for Gradle downloads
ENV GRADLE_USER_HOME=/gradle_cache

COPY ["build.gradle", "gradlew", "./"]
COPY gradle gradle
RUN chmod +x gradlew

# Ensure Gradle Wrapper uses the correct (direct GitHub) distributionUrl!
RUN ./gradlew --no-daemon downloadRepos

COPY . .
RUN chmod +x gradlew
RUN ./gradlew --no-daemon installDist

# Now switch to a minimal runtime image
FROM eclipse-temurin:21.0.5_11-jre-alpine

WORKDIR /app

COPY --from=builder /app .

EXPOSE 9555
ENTRYPOINT ["/app/build/install/hipstershop/bin/AdService"]
