"""
Prepare docker images of Train Ticket for Google Cloud deployment.
See https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling for more details.
"""
import os
import yaml
import csv

PATH_TRAIN_TICKET = "train-ticket"
PATH_DOCKER_BUILD_CONFIG = "docker-build-config"
PATH_K8S_DEPLOYMENT = "train-ticket/deployment/kubernetes-manifests/quickstart-k8s"


def build_and_push_image(path_dockerfile, image_tag, name):
    docker_build = os.system(f"docker build {path_dockerfile} -t {image_tag}")
    if docker_build != 0:
        print(f"[ERROR] Fail to build the image {name}!")
        return
    docker_push = os.system(f"docker push {image_tag}")
    if docker_push != 0:
        print(f"[ERROR] Fail to push the image {name}!")
        return


def clear_images(repo_name):
    fname_csv = "images_to_delete.csv"
    os.system(
        f"gcloud artifacts docker images list {repo_name} --format='csv[no-heading](IMAGE)' > {fname_csv}"
    )
    with open(fname_csv, newline="") as csvfile:
        images_to_delete = list(csv.reader(csvfile))
    for image in images_to_delete:
        os.system(
            f"gcloud artifacts docker images delete {image[0]} --delete-tags --quiet"
        )


def read_config(name: str):
    with open(os.path.join(PATH_DOCKER_BUILD_CONFIG, name, "config.yaml")) as stream:
        return yaml.safe_load(stream)


def read_k8s_deployment(index_part: int):
    with open(
        os.path.join(
            PATH_K8S_DEPLOYMENT, f"quickstart-ts-deployment-part{index_part}.yml"
        )
    ) as stream:
        return [doc for doc in yaml.safe_load_all(stream) if doc is not None]


def write_k8s_deployment(index_part: int, k8s_deployment):
    with open(
        os.path.join(
            PATH_K8S_DEPLOYMENT, f"gcloud-ts-deployment-part{index_part}.yaml"
        ),
        "w",
    ) as stream:
        yaml.dump_all(k8s_deployment, stream)


def update_k8s_deployment(k8s_deployment, image_tag: str, name: str):
    for i in range(len(k8s_deployment)):
        if (
            k8s_deployment[i]["kind"] == "Deployment"
            and k8s_deployment[i]["metadata"]["name"] == name
        ):
            k8s_deployment[i]["spec"]["template"]["spec"]["containers"][0][
                "image"
            ] = image_tag


def main():
    config = read_config("23102015")
    version = config["version"]
    location = config["location"]
    project_id = config["project_id"]
    repository = config["repository"]
    repo_name = f"{location}-docker.pkg.dev/{project_id}/{repository}"
    # clear_images(repo_name)

    # k8s_deployment_part_2 = read_k8s_deployment(2)
    # k8s_deployment_part_3 = read_k8s_deployment(3)

    for fname in os.listdir(PATH_TRAIN_TICKET):
        if fname.startswith("ts-"):
            path_dockerfile = os.path.join(PATH_TRAIN_TICKET, fname)
            if os.path.exists(os.path.join(path_dockerfile, "Dockerfile")):
                image_tag = f"{repo_name}/{fname}:{version}"
                build_and_push_image(path_dockerfile, image_tag, fname)
                # update_k8s_deployment(k8s_deployment_part_2, image_tag, fname)
                # update_k8s_deployment(k8s_deployment_part_3, image_tag, fname)

    # write_k8s_deployment(2, k8s_deployment_part_2)
    # write_k8s_deployment(3, k8s_deployment_part_3)


if __name__ == "__main__":
    main()
