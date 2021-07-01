import boto3
import os
import sys


def eb_deploy(env_name):
    return os.system(f"eb deploy {env_name}")
    # for Action debugging: print(f"eb deploy {env_name}")


if __name__ == "__main__":
    client = boto3.client("elasticbeanstalk")
    desc = client.describe_environments(ApplicationName="Iaso")
    eb_envs = {x["EnvironmentName"]: x for x in desc["Environments"]}

    if sys.argv[1].lower() in [x.lower() for x in eb_envs.keys()]:
        exit(eb_deploy(sys.argv[1]))

    tag_envs = {}
    target_envs = []
    for env_name, env_details in eb_envs.items():
        try:
            raw_tags = client.list_tags_for_resource(ResourceArn=env_details["EnvironmentArn"])
        except Exception as e:
            import traceback

            traceback.print_exc()
            # probably a terminated environment, just ignore
            print("Exception while browsing", env_name, "ignoring")
            continue
        tags = {x["Key"]: x["Value"] for x in raw_tags.get("ResourceTags")}
        tag_envs[env_name] = tags
        if "env" in tags and tags["env"].lower() == sys.argv[1].lower():
            target_envs.append(env_name)

    if len(target_envs) == 0:
        print("No target env found for", sys.argv[1])
    else:
        for e in target_envs:
            print("Deploying to", e)
            eb_deploy(e)
