import os
import datetime
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import storage as fb_storage
from google.cloud import storage as gc_storage

def get_nowdatetime():
    dt_now = datetime.datetime.now()
    return dt_now.strftime('%Y-%m%d-%H%M')

def get_user_dict():
    # Set dictionary.
    uid2email = {}
    # Start listing users from the beginning, 1000 at a time.
    page = auth.list_users()
    while page:
        for user in page.users:
    #         print(user.uid, user.email)
            uid2email[user.uid] = user.email
        # Get next batch of users.
        page = page.get_next_page()
    return uid2email

def list_blobs(bucket_name):
    storage_client = gc_storage.Client()

    list_of_blobs = []
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
#         print(blob.name)
        list_of_blobs.append(blob.name)
    return list_of_blobs

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = gc_storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print("{}\n => {}".format(source_blob_name, destination_file_name))

def download_all(bucket_name, blob_list, target_folder, uid2email, nowtime):
    rootdir = target_folder+"_"+nowtime
    for blob in blob_list:
        split_blob = blob.split('/')
        if len(split_blob)!=3:
            continue
        dir0 = split_blob[0]
        dir1 = split_blob[1]
        fname = split_blob[2]
        if dir0!=target_folder:
            continue
        if dir1 in uid2email.keys():
            save_email = uid2email[dir1]
            save_dir_path = os.path.join(rootdir, save_email)
            save_file_path = os.path.join(save_dir_path, fname)
            os.makedirs(save_dir_path, exist_ok=True)
            try:
                download_blob(default_bucket, blob, save_file_path)
            except Exception as e:
                print(e)
    print()
    print("=== FINISHED ===")

if __name__ == '__main__':
    ###=====###
    # ここに秘密鍵のパス
    path_to_privatekey = "/Users/<yourname>/Downloads/<privatekey.json>"
    # ここにダウンロードしたいフォルダの名前
    target_folder = "results_term0"
    ###=====###

    # Initialize default app.
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_to_privatekey
    cred = credentials.Certificate(path_to_privatekey)
    default_app = firebase_admin.initialize_app(cred, {
        'storageBucket': 'thaitone-e7817.appspot.com'
    })
    # Start.
    nowdatetime = get_nowdatetime()
    # Get list of all users.
    print("Get list of all users...")
    user_dict = get_user_dict()
    # Set default bucket.
    print("Set default bucket...")
    default_bucket = fb_storage.bucket()
    blob_list = list_blobs(default_bucket)
    print()
    print("Start downloading!!")
    download_all(
        bucket_name=default_bucket,
        blob_list=blob_list,
        target_folder=target_folder,
        uid2email=user_dict,
        nowtime=nowdatetime
    )
