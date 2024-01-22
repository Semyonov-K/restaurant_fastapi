FROM postgres:latest

ENV POSTGRES_USER test_user
ENV POSTGRES_PASSWORD test_password123
ENV POSTGRES_DB restaurantapi

EXPOSE 5432