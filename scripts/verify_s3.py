import boto3

BUCKET = "ecocart-m3-assets-habib"
REGION = "eu-north-1"

s3 = boto3.client("s3", region_name=REGION)

images = s3.list_objects_v2(
    Bucket=BUCKET, Prefix="images/"
)

descriptions = s3.list_objects_v2(
    Bucket=BUCKET, Prefix="descriptions/"
)

image_keys = [
    obj["Key"] for obj in images.get("Contents", [])
    if obj["Key"].endswith(".png")
]

description_keys = [
    obj["Key"] for obj in descriptions.get("Contents", [])
    if obj["Key"].endswith(".txt")
]

print(f"Product images: {len(image_keys)}")
print(f"Product descriptions: {len(description_keys)}")

response = s3.get_object(
    Bucket=BUCKET,
    Key="descriptions/P001.txt"
)

text = response["Body"].read().decode("utf-8")
print(f"Sample description: {text[:150]}")

assert len(image_keys) == 10
assert len(description_keys) == 10

print("SUCCESS: S3 integration verified.")
