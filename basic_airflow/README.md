# The `astro-airflow-iris` Kedro starter

## Introduction

The code in this repository demonstrates best practice when working with Kedro. It contains a Kedro starter template with some initial configuration and an example pipeline, and originates from the [Kedro Iris dataset example](https://kedro.readthedocs.io/en/stable/get_started/example_project.html). It also provides a minimum viable setup to deploy the Kedro pipeline on Airflow with [Astronomer](https://www.astronomer.io/).


### An example machine learning pipeline using only native `Kedro`

![](./images/iris_pipeline.png)

This Kedro starter uses the simple and familiar [Iris dataset](https://www.kaggle.com/uciml/iris). It contains the code for an example machine learning pipeline that trains a random forest classifier to classify an iris. 

The pipeline includes two modular pipelines: one for data engineering and one for data science.

The data engineering pipeline includes:

* A node to split the transformed data into training dataset and testing dataset using a configurable ratio

The data science pipeline includes:

* A node to train a simple multi-class logistic regression model
* A node to make predictions using this pre-trained model on the testing dataset
* A node to report the accuracy of the predictions performed by the model

```bash
pip install kedro
kedro new --starter=./kedro_template/basic_airflow
cd <my-project-name>  # change directory into newly created project directory
```

Install the required dependencies:

```bash
pip install -r src/requirements.txt
```

Now you can run the project:

```bash
#kedro mlflow init
kedro run
```

To visualise the default pipeline, run:
```bash
kedro mlflow ui
kedro viz
```

podman machine init --cpus=4 --disk-size=20 --memory=8192 -v /Volumes/My_Passport/VMO:/VMO 

podman run --name minio \
   -p 9000:9000 -d \
   -p 9090:9090 \
   -v /VMO/minio_data:/data \
   -e "MINIO_ROOT_USER=minio" \
   -e "MINIO_ROOT_PASSWORD=minio123" \
   quay.io/minio/minio server /data --console-address ":9090" 

podman stop minio | xargs docker rm