# Google-Cloud-ML-Enigne-Note

### File Structure:
- setup.py             (package installation)
- requirements.txt     (list of required packages)
- hptuning_config.yaml (for hyper parameters tunning)
- trainer (a folder, contains of:)
- - __init__.py
- - model.py (main tensorflow graph python)
- - task.py (imported by model.py, contains some arguments, ex: train file path, number of epoch ...)


### Preparation
#### Use virtual Environment (optional)
- Create virtual environment: `virtualenv myvirtualenv`
- Activate env source `myvirtualenv/bin/activate`

#### Put your train.csv and test.csv in your gcp bucker
- example: `gs://fatchur_test/train.csv` and `gs://fatchur_test/test.csv`

### GCloud configuration:
DATE=`date '+%Y%m%d_%H%M%S'`
export JOB_NAME=iris_$DATE
export GCS_JOB_DIR=gs://your-bucket-name/path/to/my/jobs/$JOB_NAME
echo $GCS_JOB_DIR
export TRAIN_FILE=gs://fatchur_test/train.csv
export EVAL_FILE=gs://fatchur_test/test.csv
export TRAIN_STEPS=1000
export EVAL_STEPS=100
export REGION=us-central1


### Run in Google Cloud ML Engine:
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


## Make Prediction
### Create model
`gcloud ml-engine models create <model-name> --regions <region>`

### Checking your tensorflow model in bucket
`gsutil ls -r $GCS_JOB_DIR/export/exporter/<folder with timestamp name>`
you should se these files:
- xxxxxxxxxx.pb
- variables/xxxxxxxx.index
- variables/xxxxxxxx.data-xxxxx-of-xxxxxx

### Generate a serving model
`export MODEL_BINARIES=$GCS_JOB_DIR/export/exporter/<folder with timestamp name>`
`gcloud ml-engine versions create <the-version> --model <model-name> --origin $MODEL_BINARIES --runtime-version 1.10` 
