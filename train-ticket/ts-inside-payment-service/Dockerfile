FROM adoptopenjdk/openjdk8:x86_64-ubuntu-jre8u292-b10

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

ADD target/ts-inside-payment-service-1.0.jar /app/
CMD ["java", "-Xmx4g", "-XX:NewRatio=1", "-XX:-UseAdaptiveSizePolicy",  "-jar", "/app/ts-inside-payment-service-1.0.jar"]

EXPOSE 18673