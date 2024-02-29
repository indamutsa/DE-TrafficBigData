# Data Engineering with Traffic Data

In this data engineering project, we will be working with traffic data from the city of Seattle. The data is dummy, hence generated but with close to the reality data found and generated in smart cities. Usually, The data is collected by the city's traffic management system and includes information about traffic flow, traffic speed, and traffic volume. The data is collected from various sensors and cameras installed throughout the city.

Our dataset will include the following data sources:

![alt text](images/vehicle.png)

- Vehicle data
- GPS data
- Camera data
- Weather data
- Emergency data

![alt text](images/architecture.png)

As seen, in the architecture diagram, the data is collected from various sources and is then ingested into Kafka which leverages the zookeeper for distributed coordination. The data is then processed using Spark and stored in Amazon S3.
From here, we leverage amazon data tech stack to store the data in a data lake and then use AWS Glue to catalog the data through crawlers and make it available for querying using Amazon Athena and Amazon Redshift.

The data is then used to generate reports and dashboards using PowerBI, Tableau and Looker Studio.

## Getting Started
