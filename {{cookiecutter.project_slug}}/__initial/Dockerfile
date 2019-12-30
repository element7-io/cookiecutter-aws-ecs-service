FROM openjdk:8-alpine

RUN apk add tzdata
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

ENV TZ Europe/Brussels
ENV LC_ALL C
ENV JAVA_OPTIONS="-XX:+UnlockExperimentalVMOptions -XX:+UseCGroupMemoryLimitForHeap -Djava.security.egd=file:/dev/./urandom"

ARG DEPENDENCY=build/raw
COPY ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY ${DEPENDENCY}/META-INF /app/META-INF
COPY ${DEPENDENCY}/BOOT-INF/classes /app

EXPOSE {{ cookiecutter.container_port }}

USER appuser
ENTRYPOINT ["java","-cp","/app:/app/lib/*","{{ cookiecutter.main_class }}"]
