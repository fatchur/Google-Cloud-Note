# Google-Cloud-ML-Enigne-Note


### A. General Python Requirements
- json
- Google API python client : `pip3 install --upgrade google-api-python-client`
- Google auth client : `pip3 install --upgrade oauth2client`


### B. MUST BE REMEMBER
All batch sizes of tensorflow graph **should be unknown** (None) 


### C. Standard ML-Engine Training 
The standard training result is ready to berved model in ml-engine without additional steps.
- [x] already in ML-Engine standard format
- [x] Must strong enough in tensorflow estimator

#### C.1 File Structure:
- setup.py             (package installation)
- requirements.txt     (list of required packages)
- hptuning_config.yaml (for hyper parameters tunning)
- trainer (a folder, contains of:)
    - `__init__.py`
    - `model.py` (main tensorflow graph python)
    - `task.py` (imported by model.py, contains some arguments, ex: train file path, number of epoch ...)

#### C.2 Preparation
##### Use virtual Environment (optional)
- Create virtual environment: `virtualenv myvirtualenv`
- Activate env source `myvirtualenv/bin/activate`

##### Put your train.csv and test.csv in your gcp bucker
- example: `gs://fatchur_test/train.csv` and `gs://fatchur_test/test.csv`

#### C.3 Training Command in Local:
```
DATE=`date '+%Y%m%d_%H%M%S'`
export JOB_NAME=iris_$DATE
export GCS_JOB_DIR=gs://your-bucket-name/path/to/my/jobs/$JOB_NAME
echo $GCS_JOB_DIR
export TRAIN_FILE=gs://fatchur_test/train.csv
export EVAL_FILE=gs://fatchur_test/test.csv
export TRAIN_STEPS=1000
export EVAL_STEPS=100
export REGION=us-central1
```

#### C.4 Training Command in Google Cloud ML Engine:
```
gcloud ml-engine jobs submit training $JOB_NAME \
    --stream-logs \
    --runtime-version 1.10 \
    --job-dir $GCS_JOB_DIR \
    --module-name trainer.task \
    --package-path trainer/ \
    --region $REGION \
    -- \
    --train-file $TRAIN_FILE \
    --eval-file $EVAL_FILE \
    --train-steps $TRAIN_STEPS \
    --eval-steps $EVAL_STEPS
```

### D. Non Standard ML-Engine training
You also can deploy your model without following the ML-engine standard format.
- [x] result model must be converted to ml-engine format
- [x] no need to know about tensorflow serving (EASY)

#### D.2 Model Preparation (Structural Data)
```python
############  serving model procedure #################
builder = tf.saved_model.builder.SavedModelBuilder('coba_mini/')

# Create aliase tensors
# tensor_info_x: for input tensor
# tensor_info_y: for output tensor
tensor_info_x = tf.saved_model.utils.build_tensor_info(LSTM.input_feature_placeholder)
tensor_info_y = tf.saved_model.utils.build_tensor_info(out)

# create prediction signature
prediction_signature = tf.saved_model.signature_def_utils.build_signature_def(
        inputs={'input': tensor_info_x},
        outputs={'output': tensor_info_y},
        method_name=tf.saved_model.signature_constants.REGRESS_METHOD_NAME)
# So your input json is:
# {"input": your features}
# REMEMBER: the shape of your feature is without batch for single request

# build frozen graph
legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')
builder.add_meta_graph_and_variables(
    session, [tf.saved_model.tag_constants.SERVING],
    signature_def_map={
        'predict_result':
        prediction_signature
    },
    legacy_init_op=legacy_init_op)
builder.save()
```

#### D.3 Model Preparation (Image Data)

#### D.4 TF Frozen Graph Model Structure 
- `saved_model.pb`
- variables
-   - `variables.index`
-   - `variables.xxxxxx-of-xxxxxx`



### E Serving-Up the Model
#### E.1 Add your model to google storage/bucket
#### E.2 Create model
`gcloud ml-engine models create <model-name> --regions <region>`

#### E.3 Checking your tensorflow model in bucket
`gsutil ls -r $GCS_JOB_DIR/export/exporter/<folder with timestamp name>`
you should se these files:
- xxxxxxxxxx.pb
- variables/xxxxxxxx.index
- variables/xxxxxxxx.data-xxxxx-of-xxxxxx

#### E.5 Generate a serving model
`export MODEL_BINARIES=$GCS_JOB_DIR/export/exporter/<folder with timestamp name>` <br>
`gcloud ml-engine versions create <the-version> --model <model-name> --origin $MODEL_BINARIES --runtime-version 1.10` 


### F Make Online Prediction
#### F.1 Online Prediction with Gcloud Command
`gcloud ml-engine predict --model <model-name> --version <model-version> --text-instances test.csv` <br>
`gcloud ml-engine predict --model <model-name> --version <model-version> --json-instances test.json`

#### F.2 Online Prediction with Python
##### F.2.1 Requirements
- Credential json
##### How to get ?
- select `IAM & admin` from hamburger menu
- select `service account`
-   -   click `create service account`
-   -   fill the name and description
-   -   click `create`
-   -   fill the role
-   -   click `continue`
-   -   click `create key`
-   -   `done`

##### F.2.2 Executing the credential json key
-   `export GOOGLE_APPLICATION_CREDENTIALS=<path to your .json key>`
-   `nano ~/.profilee` then add this: `export GOOGLE_APPLICATION_CREDENTIALS=<path to your .json key>`
-   `source ~/.bashrc`

##### F.2.3 Python Example (Case: structural data model)
```python
from googleapiclient import discovery
from googleapiclient import errors
from oauth2client.client import GoogleCredentials


def predict_json(project, model, instances, version=None):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    service = discovery.build('ml', 'v1') #, credentials=credential_json)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

PROJECT_ID  = "transmart-212604"
MODEL = "try_egg"
# the input
instance = {"input": [[ 0.58, -0.8016005 ], [ 0.58, -0.53400874], [ 0.45333335, 0.8453637 ]]}
res = predict_json(project=PROJECT_ID, model=MODEL, instances=instance, version="v5")
print (res)
```
